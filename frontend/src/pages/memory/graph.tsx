import { useEffect, useState, useRef, useMemo, useCallback } from 'react'
import dynamic from 'next/dynamic'
import Head from 'next/head'
import './graph.css'

// Dynamic import for client-side only (Next.js) - ssr: false is key
const ForceGraph2D = dynamic(() => import('react-force-graph-2d'), { ssr: false }) as any

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://api.ctxeco.com'

type GraphNode = {
    id: string
    content: string
    node_type: string
    degree: number
    metadata: Record<string, unknown>
    x?: number
    y?: number
}

type GraphEdge = {
    id: string
    source: string
    target: string
    label?: string | null
    weight: number
}

type GraphData = {
    nodes: GraphNode[]
    edges: GraphEdge[]
    stats?: {
        total_nodes: number
        total_edges: number
        node_types: Record<string, number>
        avg_degree: number
        max_degree: number
    }
}

const NODE_COLORS: Record<string, string> = {
    fact: '#00d4ff',      // Cyan for facts
    entity: '#a855f7',    // Purple for entities
    memory: '#10b981',    // Green for episodic memory
    user: '#ef4444',      // Red for User
    topic: '#f59e0b',     // Amber for topics
    meta: '#6b7280',      // Gray for metadata
}

const NODE_LABELS: Record<string, string> = {
    fact: 'Fact',
    entity: 'Entity',
    memory: 'Episode',
    user: 'User',
    topic: 'Topic',
    meta: 'Metadata',
}

export default function KnowledgeGraphPage() {
    const [data, setData] = useState<GraphData>({ nodes: [], edges: [] })
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [query, setQuery] = useState('')
    const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null)
    const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null)
    const [showStats, setShowStats] = useState(true)
    const [filterNodeType, setFilterNodeType] = useState<string>('all')
    const [minDegree, setMinDegree] = useState(0)

    const [lastQueryTimeMs, setLastQueryTimeMs] = useState<number | null>(null)
    const [lastLoadedAt, setLastLoadedAt] = useState<Date | null>(null)

    const containerRef = useRef<HTMLDivElement>(null)
    const graphRef = useRef<any>(null)
    const [dimensions, setDimensions] = useState({ width: 800, height: 600 })

    // Fetch graph data
    const fetchGraph = useCallback(async (searchQuery: string = '') => {
        setLoading(true)
        setError(null)
        try {
            const start = performance.now()
            // Call API
            const token = localStorage.getItem('token') // Attempt to get token if auth needed
            const headers: Record<string, string> = {
                'Content-Type': 'application/json'
            }
            if (token) headers['Authorization'] = `Bearer ${token}`

            const url = new URL(`${API_URL}/api/v1/memory/graph`)
            if (searchQuery) url.searchParams.append('query', searchQuery)
            url.searchParams.append('limit', '100')

            const res = await fetch(url.toString(), { headers })
            if (!res.ok) throw new Error(`API Error: ${res.statusText}`)

            const response = await res.json()

            const elapsed = performance.now() - start
            setLastQueryTimeMs(elapsed)
            setLastLoadedAt(new Date())

            // Calculate statistics if not provided by backend or verify
            const nodeTypes: Record<string, number> = response.stats?.node_types || {}
            let totalDegree = 0
            let maxDegree = 0

            if (Object.keys(nodeTypes).length === 0) {
                response.nodes.forEach((node: GraphNode) => {
                    nodeTypes[node.node_type] = (nodeTypes[node.node_type] || 0) + 1
                    totalDegree += node.degree || 0
                    maxDegree = Math.max(maxDegree, node.degree || 0)
                })
            } else {
                // Use backend provided
                maxDegree = response.stats?.max_degree || 0
                totalDegree = 0 // approximations
            }

            const stats = {
                total_nodes: response.nodes.length,
                total_edges: response.edges.length,
                node_types: nodeTypes,
                avg_degree: response.nodes.length > 0 ? (response.stats?.total_edges * 2) / response.nodes.length : 0,
                max_degree: maxDegree,
            }

            setData({
                nodes: response.nodes,
                edges: response.links || response.edges, // Backend might return 'links' due to networkx
                stats,
            })
        } catch (err: any) {
            console.error('Failed to load knowledge graph:', err)
            setError(err.message || 'Unable to load knowledge graph.')
        } finally {
            setLoading(false)
        }
    }, [])

    useEffect(() => {
        void fetchGraph(query)
    }, [query]) // Auto-fetch on query change (maybe debounce in real usage)

    // Handle resizing
    useEffect(() => {
        const updateDimensions = () => {
            if (containerRef.current) {
                setDimensions({
                    width: containerRef.current.clientWidth,
                    height: window.innerHeight - 200
                })
            }
        }

        window.addEventListener('resize', updateDimensions)
        // Initial delay to allow layout
        setTimeout(updateDimensions, 100)

        return () => window.removeEventListener('resize', updateDimensions)
    }, [])

    // Filter nodes and edges based on filters
    const filteredData = useMemo(() => {
        let filteredNodes = data.nodes.filter(node => {
            if (filterNodeType !== 'all' && node.node_type !== filterNodeType) return false
            if ((node.degree || 0) < minDegree) return false
            return true
        })

        const nodeIds = new Set(filteredNodes.map(n => n.id))
        const filteredEdges = data.edges.filter(edge =>
            nodeIds.has(edge.source as any) && nodeIds.has(edge.target as any)
            // Note: d3-force might replace source/target with objects, so check properly
        )

        // Handle object references if D3 mutated them
        const safeFilteredEdges = filteredEdges.filter(edge => {
            const s = typeof edge.source === 'object' ? (edge.source as any).id : edge.source
            const t = typeof edge.target === 'object' ? (edge.target as any).id : edge.target
            return nodeIds.has(s) && nodeIds.has(t)
        })

        return { nodes: filteredNodes, links: safeFilteredEdges }
    }, [data, filterNodeType, minDegree])

    // Node size based on degree
    const getNodeSize = useCallback((node: GraphNode) => {
        if (!data.stats) return 5
        const normalizedDegree = data.stats.max_degree > 0
            ? (node.degree || 0) / data.stats.max_degree
            : 0.5
        return 5 + normalizedDegree * 10
    }, [data.stats])

    // Get unique node types
    const nodeTypes = useMemo(() => {
        const types = new Set(data.nodes.map(n => n.node_type))
        return Array.from(types).sort()
    }, [data.nodes])

    return (
        <>
            <Head>
                <title>Graph Knowledge | ctxEco</title>
            </Head>
            <div className="memory-graph-page">
                {/* Header */}
                <div className="memory-graph-header">
                    <p style={{ fontSize: '0.75rem', letterSpacing: '0.12em', textTransform: 'uppercase', color: 'var(--color-text-muted, #888)' }}>
                        Memory
                    </p>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginTop: '0.5rem' }}>
                        <div>
                            <h2>Gk (Graph Knowledge) — Tri-Search Graph Layer</h2>
                            <p style={{ marginTop: '0.5rem', opacity: 0.8, maxWidth: '800px' }}>
                                Explore entities, facts, and relationships stored in Zep memory.
                            </p>
                        </div>
                        <button
                            onClick={() => setShowStats(!showStats)}
                            style={{
                                padding: '0.5rem 1rem',
                                background: showStats ? 'var(--color-primary, #00d4ff)' : 'rgba(255,255,255,0.1)',
                                border: '1px solid rgba(255,255,255,0.1)',
                                borderRadius: '8px',
                                color: showStats ? '#0b1020' : 'var(--color-text, #fff)',
                                cursor: 'pointer',
                                fontSize: '0.9rem'
                            }}
                        >
                            {showStats ? 'Hide' : 'Show'} Stats
                        </button>
                    </div>
                </div>

                {/* Controls */}
                <div className="memory-graph-controls">
                    <div style={{ flex: 1, minWidth: '300px' }}>
                        <input
                            type="text"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && fetchGraph(query)}
                            placeholder="Filter/Search graph facts..."
                            style={{
                                width: '100%',
                                padding: '0.75rem',
                                background: 'rgba(255,255,255,0.05)',
                                border: '1px solid rgba(255,255,255,0.1)',
                                color: 'var(--color-text, #fff)',
                                borderRadius: '8px'
                            }}
                        />
                    </div>
                    <select
                        value={filterNodeType}
                        onChange={(e) => setFilterNodeType(e.target.value)}
                        style={{
                            padding: '0.75rem',
                            background: 'rgba(255,255,255,0.05)',
                            border: '1px solid rgba(255,255,255,0.1)',
                            color: 'var(--color-text, #fff)',
                            borderRadius: '8px',
                            minWidth: '150px'
                        }}
                    >
                        <option value="all">All Types</option>
                        {nodeTypes.map(type => (
                            <option key={type} value={type}>{NODE_LABELS[type] || type}</option>
                        ))}
                    </select>
                </div>

                {/* Main Content */}
                <div className="memory-graph-main">
                    {/* Graph Visualization */}
                    <div
                        ref={containerRef}
                        className="memory-graph-viz"
                    >
                        {loading && (
                            <div style={{
                                position: 'absolute',
                                top: '50%',
                                left: '50%',
                                transform: 'translate(-50%, -50%)',
                                zIndex: 10,
                                background: 'rgba(0,0,0,0.8)',
                                padding: '1rem 2rem',
                                borderRadius: '8px',
                                color: '#00d4ff'
                            }}>
                                Loading Knowledge Graph...
                            </div>
                        )}

                        {!loading && !error && (
                            <ForceGraph2D
                                ref={graphRef}
                                width={dimensions.width}
                                height={dimensions.height}
                                graphData={filteredData}
                                nodeLabel={(node: any) => {
                                    return `${node.content}\nType: ${node.node_type}`
                                }}
                                nodeColor={(node: any) => {
                                    if (selectedNode && node.id === selectedNode.id) return '#ffffff'
                                    return NODE_COLORS[node.node_type] || '#6b7280'
                                }}
                                nodeVal={getNodeSize}
                                linkDirectionalArrowLength={4}
                                linkDirectionalArrowRelPos={1}
                                linkWidth={1}
                                linkColor={() => 'rgba(255,255,255,0.2)'}
                                backgroundColor="rgba(0,0,0,0)"
                                onNodeClick={(node: any) => {
                                    setSelectedNode(node)
                                    if (graphRef.current) {
                                        graphRef.current.centerAt(node.x, node.y, 1000)
                                        graphRef.current.zoom(2, 1000)
                                    }
                                }}
                                nodeCanvasObject={(node: any, ctx: CanvasRenderingContext2D, globalScale: number) => {
                                    const label = node.content.length > 20 ? node.content.substring(0, 20) + '...' : node.content;
                                    const fontSize = 12 / Math.sqrt(globalScale);
                                    ctx.font = `${fontSize}px Sans-Serif`;
                                    const textWidth = ctx.measureText(label).width;
                                    const bckgDimensions = [textWidth + fontSize * 0.4, fontSize * 1.4];

                                    ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
                                    // Background rectangle based on text
                                    // ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...);

                                    // Draw Node Circle
                                    ctx.beginPath();
                                    const r = Math.sqrt(getNodeSize(node)) * 2; // radius roughly
                                    ctx.arc(node.x!, node.y!, r, 0, 2 * Math.PI, false);
                                    ctx.fillStyle = (selectedNode && node.id === selectedNode.id) ? '#ffffff' : (NODE_COLORS[node.node_type] || '#6b7280');
                                    ctx.fill();

                                    // Draw Text
                                    ctx.textAlign = 'center';
                                    ctx.textBaseline = 'middle';
                                    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
                                    ctx.fillText(label, node.x!, node.y! + r + fontSize);
                                }}
                            />
                        )}

                        {error && (
                            <div style={{ color: 'red', padding: '2rem', textAlign: 'center' }}>
                                {error}
                            </div>
                        )}
                    </div>

                    {/* Sidebar */}
                    <div className="memory-graph-sidebar">
                        {selectedNode && (
                            <div className="memory-graph-panel">
                                <h3>{selectedNode.node_type.toUpperCase()}</h3>
                                <p>{selectedNode.content}</p>
                                <pre style={{ fontSize: '0.8rem', overflow: 'auto' }}>
                                    {JSON.stringify(selectedNode.metadata, null, 2)}
                                </pre>
                                <button onClick={() => setSelectedNode(null)}>Close</button>
                            </div>
                        )}

                        {showStats && data.stats && (
                            <div className="memory-graph-panel">
                                <h3>Stats</h3>
                                <div>Nodes: {data.stats.total_nodes}</div>
                                <div>Edges: {data.stats.total_edges}</div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </>
    )
}
