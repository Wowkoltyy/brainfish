import redis
from typing import List, Optional

class RedisManager:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def add_blocked_domain(self, domain: str) -> bool:
        """Add a domain to the blocked list."""
        return self.redis_client.sadd('blocked_domains', domain) > 0

    def remove_blocked_domain(self, domain: str) -> bool:
        """Remove a domain from the blocked list."""
        return self.redis_client.srem('blocked_domains', domain) > 0

    def get_blocked_domains(self) -> List[str]:
        """Get all blocked domains."""
        return list(self.redis_client.smembers('blocked_domains'))

    def is_domain_blocked(self, domain: str) -> bool:
        """Check if a domain is blocked."""
        return self.redis_client.sismember('blocked_domains', domain)

    
    # New methods for blocked-assets.json

    def get_blocked_assets(self) -> dict:
        """Get the blocked-assets.json content."""
        json_str = self.redis_client.get('blocked_assets_json')
        if json_str: return json.loads(json_str)
        return {}

    def update_blocked_assets(self, blocked_assets: dict) -> bool:
        """Update the blocked-assets.json content."""
        json_str = json.dumps(blocked_assets)
        return self.redis_client.set('blocked_assets_json', json_str)

    def add_blocked_asset(self, asset_type: str, asset_url: str) -> bool:
        """Add a new asset to the blocked-assets.json."""
        blocked_assets = self.get_blocked_assets()
        if asset_type not in blocked_assets:
            blocked_assets[asset_type] = []
        if asset_url not in blocked_assets[asset_type]:
            blocked_assets[asset_type].append(asset_url)
            return self.update_blocked_assets(blocked_assets)
        return False

    def remove_blocked_asset(self, asset_type: str, asset_url: str) -> bool:
        """Remove an asset from the blocked-assets.json."""
        blocked_assets = self.get_blocked_assets()
        if asset_type in blocked_assets and asset_url in blocked_assets[asset_type]:
            blocked_assets[asset_type].remove(asset_url)
            if not blocked_assets[asset_type]:
                del blocked_assets[asset_type]
            return self.update_blocked_assets(blocked_assets)
        return False

    
     # Whitelisted domains methods
    def add_whitelisted_domain(self, domain: str) -> bool:
        """Add a domain to the whitelist."""
        return self.redis_client.sadd('whitelisted_domains', domain) > 0

    def remove_whitelisted_domain(self, domain: str) -> bool:
        """Remove a domain from the whitelist."""
        return self.redis_client.srem('whitelisted_domains', domain) > 0

    def get_whitelisted_domains(self) -> List[str]:
        """Get all whitelisted domains."""
        return list(self.redis_client.smembers('whitelisted_domains'))

    def is_domain_whitelisted(self, domain: str) -> bool:
        """Check if a domain is whitelisted."""
        return self.redis_client.sismember('whitelisted_domains', domain)

    # Generic methods for future use

    def set_value(self, key: str, value: str) -> bool:
        """Set a key-value pair."""
        return self.redis_client.set(key, value)

    def get_value(self, key: str) -> Optional[str]:
        """Get a value by key."""
        return self.redis_client.get(key)

    def delete_key(self, key: str) -> bool:
        """Delete a key."""
        return self.redis_client.delete(key) > 0

    def add_to_set(self, set_name: str, value: str) -> bool:
        """Add a value to a set."""
        return self.redis_client.sadd(set_name, value) > 0

    def remove_from_set(self, set_name: str, value: str) -> bool:
        """Remove a value from a set."""
        return self.redis_client.srem(set_name, value) > 0

    def get_set_members(self, set_name: str) -> List[str]:
        """Get all members of a set."""
        return list(self.redis_client.smembers(set_name))

    def is_member_of_set(self, set_name: str, value: str) -> bool:
        """Check if a value is a member of a set."""
        return self.redis_client.sismember(set_name, value)

# Usage example:
# redis_manager = RedisManager(host='your_redis_host', port=your_redis_port)
# redis_manager.add_blocked_domain('example.com')
# blocked_domains = redis_manager.get_blocked_domains()