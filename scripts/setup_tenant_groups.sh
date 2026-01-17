#!/bin/bash
set -e

# ==============================================================================
# OpenContextGraph - Tenant Configuration Script
# 
# MISSION: Provision the standard "Context Ecology" taxonomy in Azure AD.
# 
# CREATES:
# 1. Functional Roles (OpenContext:Admin, etc.)
# 2. Data Access Groups (Dept:Finance, Proj:CtxEcoDev)
# 3. Agent Identities (Service Principals for Elena, Marcus, Sage)
# 4. Agent Group Assignments
# 
# NIST AI RMF: MANAGE 1.3 (RBAC/ABAC infrastructure)
# ==============================================================================

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== OpenContextGraph Tenant Setup ===${NC}"

# 1. Verify Login
echo -e "${YELLOW}Verifying Azure login...${NC}"
USER_UPN=$(az account show --query user.name -o tsv)
TENANT_ID=$(az account show --query tenantId -o tsv)
echo -e "${GREEN}Logged in as: $USER_UPN (Tenant: $TENANT_ID)${NC}"

# Function to get or create a group
get_or_create_group() {
    local group_name=$1
    local group_desc=$2
    
    echo -n "Checking group '$group_name'... "
    local group_id=$(az ad group list --display-name "$group_name" --query "[?displayName=='$group_name'].id" -o tsv)
    
    if [ -z "$group_id" ]; then
        echo -e "${YELLOW}Creating...${NC}"
        group_id=$(az ad group create --display-name "$group_name" --mail-nickname "${group_name//:/_}" --description "$group_desc" --query id -o tsv)
        echo -e "${GREEN}Created ($group_id)${NC}"
    else
        echo -e "${GREEN}Exists ($group_id)${NC}"
    fi
    eval "$3='$group_id'" # Return ID to variable
}

# Function to get or create a Service Principal (Agent)
get_or_create_agent() {
    local agent_name=$1
    local agent_desc=$2
    
    echo -n "Checking agent '$agent_name'... "
    # Check for App Registration first
    local app_id=$(az ad app list --display-name "$agent_name" --query "[?displayName=='$agent_name'].appId" -o tsv)
    
    if [ -z "$app_id" ]; then
        echo -e "${YELLOW}Creating App Registration...${NC}"
        app_id=$(az ad app create --display-name "$agent_name" --query appId -o tsv)
    fi
    
    # Check for Service Principal
    local sp_id=$(az ad sp list --display-name "$agent_name" --query "[?appId=='$app_id'].id" -o tsv)
    
    if [ -z "$sp_id" ]; then
        echo -e "${YELLOW}Creating Service Principal...${NC}"
        sp_id=$(az ad sp create --id "$app_id" --query id -o tsv)
        echo -e "${GREEN}Created SP ($sp_id)${NC}"
    else
        echo -e "${GREEN}Exists SP ($sp_id)${NC}"
    fi
    eval "$3='$sp_id'" # Return Object ID to variable
}

# 2. Provision Functional Roles
echo -e "\n${BLUE}--- Provisioning Functional Roles ---${NC}"
get_or_create_group "OpenContext:Admin" "Platform Administrators" GROUP_ADMIN
get_or_create_group "OpenContext:Analyst" "Power Users / Analysts" GROUP_ANALYST
get_or_create_group "OpenContext:User" "Standard Users" GROUP_USER

# 3. Provision Data Access Groups (Departments & Projects)
echo -e "\n${BLUE}--- Provisioning Data Access Groups ---${NC}"
get_or_create_group "Dept:Finance" "Finance Department - Confidential" GROUP_FINANCE
get_or_create_group "Dept:Engineering" "Engineering Department" GROUP_ENG
get_or_create_group "Dept:HR" "Human Resources - Restricted" GROUP_HR
get_or_create_group "Proj:CtxEcoDev" "Context Ecology Development Project" GROUP_CTXECO
get_or_create_group "Proj:Alpha" "Project Alpha - Secret" GROUP_ALPHA

# 4. Provision Agent Identities
echo -e "\n${BLUE}--- Provisioning Agent Identities ---${NC}"
get_or_create_agent "Agent:Elena" "Elena - System Architect (Finance Access)" AGENT_ELENA
get_or_create_agent "Agent:Marcus" "Marcus - Engineering Lead (Dev Access)" AGENT_MARCUS
get_or_create_agent "Agent:Sage" "Sage - Creative Storyteller (Analyst Access)" AGENT_SAGE

# 5. Assign Agents to Groups
echo -e "\n${BLUE}--- Assigning Agents to Groups ---${NC}"

assign_member() {
    local group_id=$1
    local member_id=$2
    local group_name=$3
    local member_name=$4
    
    echo -n "Assigning $member_name to $group_name... "
    # Check membership
    local is_member=$(az ad group member check --group "$group_id" --member-id "$member_id" --query value -o tsv)
    
    if [ "$is_member" == "true" ]; then
        echo -e "${GREEN}Already assigned${NC}"
    else
        az ad group member add --group "$group_id" --member-id "$member_id"
        echo -e "${GREEN}Assigned${NC}"
    fi
}

# Elena -> Finance (For financial reports)
assign_member "$GROUP_FINANCE" "$AGENT_ELENA" "Dept:Finance" "Agent:Elena"
# Marcus -> CtxEcoDev (For repo access)
assign_member "$GROUP_CTXECO" "$AGENT_MARCUS" "Proj:CtxEcoDev" "Agent:Marcus"
# Sage -> Analyst (For story generation across broad data)
assign_member "$GROUP_ANALYST" "$AGENT_SAGE" "OpenContext:Analyst" "Agent:Sage"

# 6. Assign Current User (Admin)
echo -e "\n${BLUE}--- Assigning Current User ($USER_UPN) ---${NC}"
CURRENT_USER_ID=$(az ad signed-in-user show --query id -o tsv)
assign_member "$GROUP_ADMIN" "$CURRENT_USER_ID" "OpenContext:Admin" "Me"
# Assign to all depts for testing/CEO role
assign_member "$GROUP_FINANCE" "$CURRENT_USER_ID" "Dept:Finance" "Me"
assign_member "$GROUP_ENG" "$CURRENT_USER_ID" "Dept:Engineering" "Me"
assign_member "$GROUP_CTXECO" "$CURRENT_USER_ID" "Proj:CtxEcoDev" "Me"

echo -e "\n${GREEN}=== Tenant Setup Complete ===${NC}"
echo "You can now use these Groups in Ingestion ACLs (e.g., ['Dept:Finance'])."
