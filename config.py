import json
from pathlib import Path
from typing import Dict, Any, List

class Config:
    
    def __init__(self, config_path: "config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()        

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file, create default if not exists"""
        if not self.config_path.exists():
            print(f"Config file not found, creating default: {self.config_path}")
            self._create_default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                print(f"Loaded configuration from {self.config_path}")
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")
            print("Using default configuration")
            return EXAMPLE_CONFIG
    
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