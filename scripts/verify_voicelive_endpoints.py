import asyncio
import sys
import os
import logging
from pathlib import Path

# Add backend to path (so 'from core' and 'from voice' work)
sys.path.append(str(Path(__file__).parent.parent / "backend"))
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def verify_endpoints():
    print(f"🔍 Verifying VoiceLive Endpoints...")
    
    try:
        # Import after path setup
        from voice.voicelive_service import voicelive_service
        from api.routes.voice import get_realtime_token, get_avatar_ice_credentials, TokenRequest, AvatarIceRequest
        
        # 1. Check Configuration
        print(f"\n1️⃣  Checking Configuration...")
        if not voicelive_service.is_configured:
            print(f"❌ VoiceLive service NOT configured.")
            print(f"   Endpoint: {voicelive_service.endpoint}")
            print(f"   Key: {'***' if voicelive_service.key else 'None'}")
            return
        print(f"✅ VoiceLive configured: {voicelive_service.endpoint}")
        print(f"   Project: {voicelive_service.project_name or 'None (Standard)'}")
        print(f"   Region: {voicelive_service.speech_region or 'Auto'}")
        
        # 2. Verify Realtime Token Generation (Browser Direct)
        print(f"\n2️⃣  Verifying Realtime Token (TokenRequest)...")
        token_request = TokenRequest(
            agent_id="elena",
            modalities=["audio", "text", "video"] # Request video to trigger potential video-specific logic
        )
        
        try:
            token_response = await get_realtime_token(token_request)
            print(f"✅ Token Generated Successfully!")
            print(f"   Endpoint: {token_response.endpoint}")
            print(f"   Token: {token_response.token[:10]}... (len: {len(token_response.token)})")
        except Exception as e:
            print(f"❌ Token Generation Failed: {e}")
            import traceback
            traceback.print_exc()

        # 3. Verify Avatar ICE Credentials
        print(f"\n3️⃣  Verifying Avatar ICE Credentials...")
        try:
            ice_response = await get_avatar_ice_credentials(AvatarIceRequest(agent_id="elena"))
            print(f"✅ ICE Credentials Retrieved!")
            print(f"   ICE Servers: {len(ice_response.urls)}")
            print(f"   Username: {ice_response.username[:10]}...")
            print(f"   TTL: {ice_response.ttl}")
        except Exception as e:
            print(f"❌ ICE Credentials Failed: {e}")
            print(f"   Note: This requires a valid Azure Speech Key or Managed Identity with Speech access.")
            import traceback
            traceback.print_exc()

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("   Ensure you are running from the project root or have dependencies installed.")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(verify_endpoints())
