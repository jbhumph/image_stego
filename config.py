import json
from pathlib import Path
from typing import Dict, Any, List

EXAMPLE_CONFIG = {
    "general": {
        "verbose_mode": True,
        "show_preview": True,
        "auto_backup": False,
        "preserve_metadata": False
    },
    "embedding": {
        "delimiter_type": "null_terminator",  # "null_terminator", "magic_sequence", "length_prefix"
        "magic_sequence": "1111111100000000",
        "channels_to_use": ["R", "G", "B"],  # Which color channels
        "bits_per_channel": 1,  # How many LSBs to use (1-4)
        "embedding_pattern": "sequential",  # "sequential", "random", "spiral"
        "skip_pixels": 0,  # Skip every N pixels (0 = use all)
        "capacity_warning_threshold": 80  # Warn if using >80% of image capacity
    },
    "security": {
        "encryption_enabled": False,
        "encryption_algorithm": "AES",  # "AES", "XOR", "none"
        "password_hash_algorithm": "SHA256"
    },
    "file_handling": {
        "supported_input_formats": [".png", ".bmp", ".tiff", ".jpg", ".jpeg"],
        "default_output_format": ".png",
        "compression_level": 6,  # PNG compression (0-9)
        "max_message_length": 10000,  # Maximum characters
        "min_image_size": [100, 100],  # [width, height] minimum
        "output_filename_template": "{original_name}_encoded{extension}"
    },
    "validation": {
        "strict_mode": True,  # Strict validation of inputs
        "allow_overwrite": False,  # Allow overwriting existing files
        "verify_embedding": True  # Test decode after encoding
    },
    "logging": {
        "save_logs": False,
        "log_file": "steganography.log",
        "log_level": "INFO"  # DEBUG, INFO, WARNING, ERROR
    }
}

class Config:

    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()        

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file, create default if not exists or corrupt"""
        # If file doesn't exist or is empty, create default and return it
        if not self.config_path.exists() or self.config_path.stat().st_size == 0:
            print(f"Config file not found or empty, creating default: {self.config_path}")
            self._create_default_config()
            return EXAMPLE_CONFIG.copy()

        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                print(f"Loaded configuration from {self.config_path}")
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")
            # Try to back up the corrupt file so user can inspect it
            try:
                backup_path = self.config_path.with_suffix(self.config_path.suffix + ".bak")
                self.config_path.replace(backup_path)
                print(f"Moved corrupt config to {backup_path}")
            except Exception:
                # If backup fails, ignore and proceed to recreate default
                pass

            print("Creating default configuration")
            self._create_default_config()
            return EXAMPLE_CONFIG.copy()
    
    def _create_default_config(self):
        """Create default config file"""
        with open(self.config_path, 'w') as f:
            json.dump(EXAMPLE_CONFIG, f, indent=4)

    def get(self, section: str, key: str, default=None):
        """Get configuration value with dot notation"""
        try:
            return self.config[section][key]
        except KeyError:
            return default
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section"""
        return self.config.get(section, {})
    
    def set(self, section: str, key: str, value: Any):
        """Set configuration value"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
    
    def save(self):
        """Save current configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
        print(f"Configuration saved to {self.config_path}")
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []
        
        # Validate file handling
        max_length = self.get('file_handling', 'max_message_length', 0)
        if max_length <= 0:
            issues.append("max_message_length must be positive")
        
        min_size = self.get('file_handling', 'min_image_size', [0, 0])
        if len(min_size) != 2 or min_size[0] <= 0 or min_size[1] <= 0:
            issues.append("min_image_size must be [width, height] with positive values")
        
        # Validate embedding settings
        channels = self.get('embedding', 'channels_to_use', [])
        if not channels or not all(c in ['R', 'G', 'B'] for c in channels):
            issues.append("channels_to_use must contain valid channels (R, G, B)")
        
        bits_per_channel = self.get('embedding', 'bits_per_channel', 1)
        if not 1 <= bits_per_channel <= 4:
            issues.append("bits_per_channel must be between 1 and 4")
        
        return issues
    
    