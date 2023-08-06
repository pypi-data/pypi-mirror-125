# Sample local Vault config.

ui = true
disable_mlock = true

storage "raft" {
  path    = "./src/strigiform/secrets/data/raft"
  node_id = "node1"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = "true"
}

api_addr = "http://127.0.0.1:8200"
cluster_addr = "https://127.0.0.1:8201"
