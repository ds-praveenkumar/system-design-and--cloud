import hashlib
import bisect

class CircularHashing:
    def __init__( self, servers, num_replicas=3 ):
        self.num_replicas = num_replicas
        self.ring = {}
        self.sorted_keys = []
        self.servers = set()
        for server in servers:
            self.add_server( server )
            
    def __repr__(self) -> str:
        for server in self.sorted_keys:
            print( server )
        
    def _hash( self , key ):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_server( self , server ):
        
        self.servers.add( server )
        for i in range(self.num_replicas):
            hash_value = self._hash( f"server-{i}")
            self.ring[hash_value] = server
            bisect.insort(self.sorted_keys, hash_value)
            
    def remove_server( self, server ):        
        
        if server in self.servers:
            self.servers.remove(server)
            for i in range(self.num_replicas):
                hash_val = self._hash(f"server-{i}")
                self.ring.pop(hash_val, None)
                self.sorted_keys.remove(hash_val) 
                
    def get_server( self, key ):
                       
        if not self.ring:
            return None
        
        hash_val = self._hash(key)
        index = bisect.bisect(self.sorted_keys, hash_val ) % len( self.sorted_keys)
        return self.ring[self.sorted_keys[index]]
    
    
if __name__ == '__main__':
    servers = ["S0",  "S1"]
    ch = CircularHashing(servers, 3)
    for server in ch.sorted_keys:
        print( server)