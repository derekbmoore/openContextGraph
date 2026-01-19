"""
Voice Configuration Validator

Validates voice and avatar configuration based on deployment guide requirements.
Provides helpful error messages that reference the troubleshooting guide.

Reference: docs/operations/avatar_voice_deployment_guide.md
"""

import logging
import re
from typing import List, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of a configuration validation check"""
    is_valid: bool
    error_message: Optional[str] = None
    warning_message: Optional[str] = None
    fix_suggestion: Optional[str] = None


class VoiceConfigValidator:
    """
    Validates voice and avatar configuration based on deployment guide.

    Checks:
    - Azure Speech region for avatar support
    - VoiceLive endpoint format
    - Required environment variables
    - Common misconfigurations
    """

    # Supported regions for Avatar (WebRTC video)
    # Reference: avatar_voice_deployment_guide.md Section 2.1
    AVATAR_SUPPORTED_REGIONS = ["westus2", "westeurope", "southeastasia"]

    # Standard Speech regions (no avatar support)
    STANDARD_REGIONS = ["eastus", "eastus2", "westus", "centralus", "northeurope"]

    def __init__(self):
        pass

    def validate_speech_region(self, region: Optional[str], avatar_required: bool = False) -> ValidationResult:
        """
        Validate Azure Speech region for avatar support.

        Args:
            region: Azure Speech region (e.g., "westus2")
            avatar_required: Whether avatar functionality is required

        Returns:
            ValidationResult with validation status and helpful messages
        """
        if not region:
            return ValidationResult(
                is_valid=False,
                error_message="AZURE_SPEECH_REGION not configured",
                fix_suggestion=(
                    "Set AZURE_SPEECH_REGION to 'westus2' (recommended for avatar support). "
                    "See docs/operations/avatar_voice_deployment_guide.md Section 2.2"
                )
            )

        region_lower = region.lower().strip()

        # Check if region supports avatar
        if avatar_required and region_lower not in self.AVATAR_SUPPORTED_REGIONS:
            # Check if it's a known standard region (common misconfiguration)
            if region_lower in self.STANDARD_REGIONS:
                return ValidationResult(
                    is_valid=False,
                    error_message=f"Avatar Region Mismatch: '{region}' does not support Avatar WebRTC",
                    fix_suggestion=(
                        f"Avatar requires one of: {', '.join(self.AVATAR_SUPPORTED_REGIONS)}. "
                        f"You're using '{region}' which is a standard Speech region. "
                        f"Deploy a new Speech resource in 'westus2' (recommended). "
                        f"See troubleshooting guide: docs/operations/avatar_voice_deployment_guide.md Section 5"
                    )
                )
            else:
                return ValidationResult(
                    is_valid=False,
                    error_message=f"Unsupported Avatar region: '{region}'",
                    fix_suggestion=(
                        f"Avatar requires one of: {', '.join(self.AVATAR_SUPPORTED_REGIONS)}. "
                        f"Change AZURE_SPEECH_REGION to 'westus2' (recommended). "
                        f"See docs/operations/avatar_voice_deployment_guide.md Section 2.1"
                    )
                )

        # Valid region for avatar or avatar not required
        if region_lower in self.AVATAR_SUPPORTED_REGIONS:
            return ValidationResult(
                is_valid=True,
                warning_message=None
            )
        elif region_lower in self.STANDARD_REGIONS:
            return ValidationResult(
                is_valid=True,
                warning_message=(
                    f"Region '{region}' does not support Avatar video. "
                    f"Audio-only mode will work, but avatar will not be available."
                )
            )
        else:
            return ValidationResult(
                is_valid=True,
                warning_message=f"Unknown region '{region}'. Verify it's a valid Azure Speech region."
            )

    def validate_voicelive_endpoint(self, endpoint: Optional[str]) -> ValidationResult:
        """
        Validate VoiceLive endpoint format.

        Args:
            endpoint: VoiceLive endpoint URL

        Returns:
            ValidationResult with validation status and endpoint type
        """
        if not endpoint:
            return ValidationResult(
                is_valid=False,
                error_message="AZURE_VOICELIVE_ENDPOINT not configured",
                fix_suggestion=(
                    "Set AZURE_VOICELIVE_ENDPOINT to your Azure AI Services endpoint. "
                    "Format: wss://{ai-services-resource-name}.services.ai.azure.com/voice-live/realtime?api-version=2024-10-01-preview&model=gpt-realtime "
                    "See docs/operations/avatar_voice_deployment_guide.md Section 2.2"
                )
            )

        endpoint_lower = endpoint.lower().rstrip('/')

        # Check endpoint format
        if "services.ai.azure.com" in endpoint_lower:
            # Unified endpoint (recommended)
            # Validate API version
            if "api-version" in endpoint_lower:
                match = re.search(r"api-version=([^&]+)", endpoint_lower)
                if match:
                    api_version = match.group(1)
                    if api_version != "2024-10-01-preview":
                        return ValidationResult(
                            is_valid=True,
                            warning_message=(
                                f"API version '{api_version}' detected. "
                                f"Recommended version is '2024-10-01-preview'. "
                                f"See docs/operations/avatar_voice_deployment_guide.md Section 2.2"
                            )
                        )

            return ValidationResult(
                is_valid=True,
                warning_message=None
            )

        elif "openai.azure.com" in endpoint_lower:
            # Direct OpenAI endpoint
            return ValidationResult(
                is_valid=True,
                warning_message="Using direct OpenAI endpoint. This is valid for audio-only mode."
            )

        elif "azure-api.net" in endpoint_lower:
            # APIM gateway (treat as unified)
            return ValidationResult(
                is_valid=True,
                warning_message="Using APIM gateway endpoint. Verify it proxies to correct backend."
            )

        else:
            return ValidationResult(
                is_valid=False,
                error_message=f"Invalid VoiceLive endpoint format: {endpoint[:50]}...",
                fix_suggestion=(
                    "Endpoint must be either:\n"
                    "  - Unified: *.services.ai.azure.com\n"
                    "  - Direct: *.openai.azure.com\n"
                    "  - APIM: *.azure-api.net\n"
                    "See docs/operations/avatar_voice_deployment_guide.md Section 2.2"
                )
            )

    def validate_authentication(
        self,
        voicelive_key: Optional[str],
        speech_key: Optional[str],
        has_managed_identity: bool = False
    ) -> ValidationResult:
        """
        Validate authentication configuration.

        Args:
            voicelive_key: VoiceLive API key
            speech_key: Speech Service API key (required for avatar)
            has_managed_identity: Whether Managed Identity is available

        Returns:
            ValidationResult with validation status
        """
        # Check VoiceLive authentication
        if not voicelive_key and not has_managed_identity:
            return ValidationResult(
                is_valid=False,
                error_message="No VoiceLive authentication configured",
                fix_suggestion=(
                    "Set either:\n"
                    "  - AZURE_VOICELIVE_KEY (for POC/staging), OR\n"
                    "  - Enable Managed Identity (for production)\n"
                    "See docs/operations/avatar_voice_deployment_guide.md Section 2.2"
                )
            )

        # Check Speech authentication (required for avatar)
        if not speech_key:
            return ValidationResult(
                is_valid=True,
                warning_message=(
                    "AZURE_SPEECH_KEY not configured. Avatar video will not be available. "
                    "Audio-only mode will work. "
                    "See docs/operations/avatar_voice_deployment_guide.md Section 2.2"
                )
            )

        return ValidationResult(is_valid=True)

    def validate_voice_config(
        self,
        voicelive_endpoint: Optional[str],
        voicelive_key: Optional[str],
        speech_key: Optional[str],
        speech_region: Optional[str],
        avatar_required: bool = False,
        has_managed_identity: bool = False
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Comprehensive validation of voice configuration.

        Args:
            voicelive_endpoint: VoiceLive endpoint URL
            voicelive_key: VoiceLive API key
            speech_key: Speech Service API key
            speech_region: Azure Speech region
            avatar_required: Whether avatar functionality is required
            has_managed_identity: Whether Managed Identity is available

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        errors = []
        warnings = []

        # Validate VoiceLive endpoint
        endpoint_result = self.validate_voicelive_endpoint(voicelive_endpoint)
        if not endpoint_result.is_valid:
            errors.append(f"❌ {endpoint_result.error_message}")
            if endpoint_result.fix_suggestion:
                errors.append(f"   Fix: {endpoint_result.fix_suggestion}")
        elif endpoint_result.warning_message:
            warnings.append(f"⚠️  {endpoint_result.warning_message}")

        # Validate Speech region
        region_result = self.validate_speech_region(speech_region, avatar_required)
        if not region_result.is_valid:
            errors.append(f"❌ {region_result.error_message}")
            if region_result.fix_suggestion:
                errors.append(f"   Fix: {region_result.fix_suggestion}")
        elif region_result.warning_message:
            warnings.append(f"⚠️  {region_result.warning_message}")

        # Validate authentication
        auth_result = self.validate_authentication(voicelive_key, speech_key, has_managed_identity)
        if not auth_result.is_valid:
            errors.append(f"❌ {auth_result.error_message}")
            if auth_result.fix_suggestion:
                errors.append(f"   Fix: {auth_result.fix_suggestion}")
        elif auth_result.warning_message:
            warnings.append(f"⚠️  {auth_result.warning_message}")

        is_valid = len(errors) == 0

        return is_valid, errors, warnings


# Global validator instance
validator = VoiceConfigValidator()
