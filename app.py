import streamlit as st

# CockroachDB Simulator - 100 question MCQ Quiz
# Scoring: +10 for correct, 0 for wrong
# After submission, the app shows which answers were correct and which were wrong.

QUESTIONS = [
    {"q": "CockroachDB is primarily designed to provide:",
     "opts": ["Strong consistency and horizontal scalability", "Eventual consistency and vertical scaling", "In-memory data replication", "Manual sharding only"],
     "ans": "A"},

    {"q": "Which consensus algorithm does CockroachDB use?",
     "opts": ["Paxos", "Raft", "ZAB", "Two-Phase Commit"],
     "ans": "B"},

    {"q": "A CockroachDB cluster is composed of:",
     "opts": ["Masters and slaves", "NameNodes and DataNodes", "Identical nodes with no masters", "Primary and secondary shards"],
     "ans": "C"},

    {"q": "CockroachDB stores data in units called:",
     "opts": ["Shards", "Ranges", "Segments", "Buckets"],
     "ans": "B"},

    {"q": "What is the default SQL port for CockroachDB?",
     "opts": ["5432", "26257", "8080", "3306"],
     "ans": "B"},

    {"q": "Which isolation level is used by CockroachDB by default?",
     "opts": ["Read uncommitted", "Read committed", "Snapshot isolation", "Serializable"],
     "ans": "D"},

    {"q": "CockroachDB uses which clock mechanism to order events?",
     "opts": ["Logical Clock", "NTP only", "Hybrid Logical Clock (HLC)", "CRDT clock"],
     "ans": "C"},

    {"q": "The CockroachDB admin UI is available on which default port?",
     "opts": ["8080", "26257", "443", "80"],
     "ans": "A"},

    {"q": "How many replicas are created by default for each range?",
     "opts": ["1", "2", "3", "5"],
     "ans": "C"},

    {"q": "Which CLI is the primary tool for interacting with CockroachDB?",
     "opts": ["cockroach", "crdbctl", "cockctl", "crdb-cli"],
     "ans": "A"},

    {"q": "Which feature lets CockroachDB survive datacenter failures?",
     "opts": ["Asynchronous replication", "Replication across multiple nodes/zones", "Single primary master", "Periodic snapshots only"],
     "ans": "B"},

    {"q": "What is a leaseholder in CockroachDB?",
     "opts": ["The node that holds the range leader for serving reads/writes", "A temporary lock file", "A backup snapshot owner", "A schema migration controller"],
     "ans": "A"},

    {"q": "Range splits occur in CockroachDB when:",
     "opts": ["A node is added", "A range grows beyond target size", "You run ALTER TABLE", "You compact data manually"],
     "ans": "B"},

    {"q": "CockroachDB transactions are coordinated using:",
     "opts": ["Two-phase commit (2PC) internally with Raft", "Simple single-node commit", "External transaction manager", "CRDT replication"],
     "ans": "A"},

    {"q": "To simulate failures in the CockroachDB Simulator you would use:",
     "opts": ["SQL injection", "Fault injection APIs in the simulator", "Cloud failure emulator only", "Manual node shutdowns only"],
     "ans": "B"},

    {"q": "Which of the following is TRUE about CockroachDB nodes?",
     "opts": ["They are heterogeneous by role (master/worker)", "They are identical and peer-equal", "Only one node can accept writes", "They require external coordination service"],
     "ans": "B"},

    {"q": "The smallest unit that Raft replicates is a:",
     "opts": ["Database", "Table", "Range/replica", "Row"],
     "ans": "C"},

    {"q": "Which of these commands starts a local cockroach node?",
     "opts": ["cockroach start", "cockroach init", "cockroach run", "cockroach up"],
     "ans": "A"},

    {"q": "What is the typical size target for a range before it splits?",
     "opts": ["64KB", "64MB", "1GB", "10GB"],
     "ans": "B"},

    {"q": "CockroachDB's survivability strategy primarily relies on:",
     "opts": ["Frequent backups", "Synchronous replication and consensus", "Client retries only", "Single-region deployments"],
     "ans": "B"},

    {"q": "Which storage flag specifies where node data lives?",
     "opts": ["--data-dir", "--store", "--path", "--storage-dir"],
     "ans": "B"},

    {"q": "How does CockroachDB handle schema changes?",
     "opts": ["Blocking all writes during ALTER", "Online schema changes with background work", "Requires cluster downtime", "Manual migration scripts only"],
     "ans": "B"},

    {"q": "Which statement about multi-region deployments is TRUE?",
     "opts": ["They reduce write latency globally automatically", "They require configuring locality and zone configs", "They don't support transactional guarantees", "They only work in cloud providers"],
     "ans": "B"},

    {"q": "Which SQL feature is NOT supported in CockroachDB?",
     "opts": ["Standard SQL SELECT/INSERT", "Stored procedures (PL/pgSQL)", "Transactions", "Secondary indexes"],
     "ans": "B"},

    {"q": "CockroachDB's backup tool is invoked with which subcommand?",
     "opts": ["cockroach dump", "cockroach backup", "cockroach snapshot", "cockroach export"],
     "ans": "B"},

    {"q": "What does the 'crdb_internal' virtual schema expose?",
     "opts": ["User tables only", "Internal metrics/state and debug info", "Only performance traces", "External system catalogs"],
     "ans": "B"},

    {"q": "Which of these helps reduce transaction contention?",
     "opts": ["Using large transactions frequently", "Choosing appropriate primary keys and partitioning", "Turning off replication", "Increasing range size"],
     "ans": "B"},

    {"q": "Which component elects a leader for a Raft group?",
     "opts": ["The SQL layer", "The network layer", "Raft protocol among replicas", "External election service"],
     "ans": "C"},

    {"q": "What happens when a node rejoins after being offline?",
     "opts": ["It discards all data and starts fresh", "It catches up via Raft log replication and snapshots", "Manual rsync is required", "The cluster must be restarted"],
     "ans": "B"},

    {"q": "Which of these is a common cause of hotspots?",
     "opts": ["Uniformly distributed primary keys", "Sequential primary keys causing writes to single range", "Having 3 replicas", "Using indexes"],
     "ans": "B"},

    {"q": "Which index type is supported in CockroachDB?",
     "opts": ["Hash indexes only", "Secondary (non-clustered) indexes", "Materialized views only", "No indexes supported"],
     "ans": "B"},

    {"q": "How are zone configurations used?",
     "opts": ["To configure replication/locality constraints and constraints for ranges", "To set SQL user permissions", "To create backups", "To define SQL schemas"],
     "ans": "A"},

    {"q": "Which statement is true about secondary indexes and transactions?",
     "opts": ["Secondary indexes are updated outside transactions", "Secondary indexes are updated transactionally with base table writes", "Secondary indexes require manual maintenance", "CockroachDB does not support secondary indexes in transactions"],
     "ans": "B"},

    {"q": "The recommended way to load test CockroachDB is using:",
     "opts": ["Manual INSERT loops only", "CockroachDB workload tool (workload) or other load generators", "Only via the admin UI", "Single-threaded clients"],
     "ans": "B"},

    {"q": "Which metric indicates node memory pressure?",
     "opts": ["sql_queries_total", "rss or memory RSS metrics via monitor", "range_count", "replication_latency"],
     "ans": "B"},

    {"q": "How are backups restored in CockroachDB?",
     "opts": ["cockroach restore", "cockroach import", "cockroach load", "cockroach recover"],
     "ans": "A"},

    {"q": "What is a common technique to avoid sequential-key hotspots?",
     "opts": ["Use UUIDs or hash prefixes", "Decrease replication factor", "Increase range target size drastically", "Disable range splits"],
     "ans": "A"},

    {"q": "CockroachDB's SQL engine is compatible with which database's dialect?",
     "opts": ["MySQL", "PostgreSQL", "Oracle", "SQL Server"],
     "ans": "B"},

    {"q": "Which of the following is true about constraints in CockroachDB?",
     "opts": ["FOREIGN KEY constraints are not supported", "NOT NULL and UNIQUE constraints are supported", "CHECK constraints are not supported", "All constraints are enforced only client-side"],
     "ans": "B"},

    {"q": "What purpose do split and scatter serve?",
     "opts": ["Split a range and move it to appropriate nodes to balance load", "Create backups", "Compact data", "Promote a leader replica"],
     "ans": "A"},

    {"q": "Which tool can you use to view live diagnostics and traces?",
     "opts": ["cockroach doctor", "admin UI and debug pages", "crdb-scan", "pg_stat_activity only"],
     "ans": "B"},

    {"q": "Which is true about change data capture (CDC) in CockroachDB?",
     "opts": ["Not supported", "Supported via changefeeds", "Only available in OSS older versions", "Requires external agent always"],
     "ans": "B"},

    {"q": "Which command shows cluster health and node status?",
     "opts": ["cockroach node status", "cockroach debug health", "cockroach cluster check", "cockroach status"],
     "ans": "A"},

    {"q": "How are historical MVCC timestamps used?",
     "opts": ["For time travel queries and transaction ordering", "Only for backups", "To store schema versions", "They aren't used"],
     "ans": "A"},

    {"q": "What does the 'scatter' operation do?",
     "opts": ["Compacts range data", "Moves ranges to random/balanced nodes to reduce hotspots", "Deletes ranges", "Splits ranges"],
     "ans": "B"},

    {"q": "Which of the following increases write throughput horizontally?",
     "opts": ["Adding more CPU to a single node", "Adding nodes to the cluster", "Increasing the range target size only", "Disabling Raft"],
     "ans": "B"},

    {"q": "What is the effect of high read reparations?",
     "opts": ["Improves cluster stability", "Indicates stale replicas may be behind and causing performance issues", "Increases write durability", "No effect"],
     "ans": "B"},

    {"q": "Which of these is a best practice for schema design to avoid contention?",
     "opts": ["Use monotonic sequence as primary key for high-volume writes", "Use composite keys and design to spread writes across ranges", "Use a single big table for all workloads", "Avoid indexes entirely"],
     "ans": "B"},

    {"q": "Which of these is true about distributed SQL execution?",
     "opts": ["All queries run on a single node only", "CockroachDB can distribute parts of query execution across nodes", "Distributed execution is disabled by default and cannot be enabled", "Only joins are distributed"],
     "ans": "B"},

    {"q": "What is the role of the 'intent' in CockroachDB transactions?",
     "opts": ["They are temporary write markers preventing conflicts until commit", "Permanent locks on rows", "A backup artifact", "A client-side token"],
     "ans": "A"},

    {"q": "Which of the following can be used to limit replication to a set of nodes?",
     "opts": ["Zone configs and constraints", "ALTER REPLICATION TO", "Replica sets in UI only", "SQL GRANT"],
     "ans": "A"},

    {"q": "Which storage engine does CockroachDB use internally?",
     "opts": ["RocksDB (Pebble in newer versions)", "InnoDB", "LevelDB only", "LMDB"],
     "ans": "A"},

    {"q": "What is the purpose of a snapshot in Raft/CockroachDB?",
     "opts": ["Permanent backup of cluster", "A compacted state transfer mechanism to bring replicas up to date", "To split ranges", "To create indexes"],
     "ans": "B"},

    {"q": "Which tuning option helps reduce write amplification at the RocksDB/Pebble layer?",
     "opts": ["Increasing GC TTL for MVCC","Tuning compaction/engine settings","Disabling replication","Increasing range count"],
     "ans": "B"},

    {"q": "Why would you use locality tags (attributes) on nodes?",
     "opts": ["To enforce topology-aware replication and prefer local reads/writes", "To control SQL permissions", "To change SQL dialect per node", "To disable Raft on certain nodes"],
     "ans": "A"},

    {"q": "Which statement about IMPORT/EXPORT is true?",
     "opts": ["IMPORT loads data into the cluster from external storage", "EXPORT imports data into external system", "IMPORT/EXPORT are deprecated and removed", "They are only available in enterprise edition"],
     "ans": "A"},

    {"q": "CockroachDB automatically rebalances ranges when:",
     "opts": ["Manual trigger only", "It detects imbalance across stores and uses the rebalancer", "Cluster is idle", "Whenever a query runs"],
     "ans": "B"},

    {"q": "Which of these is a sign of long GC pause issues affecting CockroachDB?",
     "opts": ["Increased SQL latency and stalled compactions", "Lower disk usage", "More splits", "Fewer ranges"],
     "ans": "A"},

    {"q": "A changefeed is used for:",
     "opts": ["Streaming CDC of table changes to external sinks", "Database backups", "Compacting ranges", "Managing nodes"],
     "ans": "A"},

    {"q": "How does CockroachDB ensure transactional serializability globally?",
     "opts": ["By using per-row locks only", "By combining HLC timestamps with Raft and transaction coordination", "By allowing only single-node writes", "By delaying commits for a fixed time"],
     "ans": "B"},

    {"q": "What is a common troubleshooting step when experiencing high latency?",
     "opts": ["Increase range size", "Check for hotspots, network issues, and CPU/memory pressure", "Disable replication", "Reduce number of nodes"],
     "ans": "B"},

    {"q": "Which of these is needed to perform an online schema migration safely?",
     "opts": ["Take cluster offline", "Use built-in online schema change operations and checkbackfills", "Drop indexes first always", "Stop replication"],
     "ans": "B"},

    {"q": "What does 'range lease' minimize?",
     "opts": ["Number of bytes stored", "Coordination hops for consistent reads by granting a leaseholder", "Number of replicas", "Frequency of backups"],
     "ans": "B"},

    {"q": "Which of the following operations is expensive and may run in the background after an index creation?",
     "opts": ["Immediate writes to the index only", "Backfill to populate the index", "Drop table operations", "Replica replacement"],
     "ans": "B"},

    {"q": "Which command helps compact and free MVCC across ranges?",
     "opts": ["SCRUB", "GC and manual compaction via debug or admin APIs", "VACUUM FULL", "OPTIMIZE TABLE"],
     "ans": "B"},

    {"q": "Which of these could cause Raft leadership churn?",
     "opts": ["Stable network", "Frequent node restarts or flapping network", "Low CPU usage", "Too many replicas"],
     "ans": "B"},

    {"q": "Which SQL command can you use to examine table statistics/help the optimizer?",
     "opts": ["SHOW STATISTICS", "EXPLAIN ANALYZE and SHOW STATISTICS", "DESCRIBE STATS", "ANALYZE TABLE only"],
     "ans": "B"},

    {"q": "What tool/library does CockroachDB use to back up to cloud storage?",
     "opts": ["Built-in backup to cloud (S3/GCS/Azure) via cockroach backup", "Third-party only", "Manual rsync to cloud", "It does not support cloud backups"],
     "ans": "A"},

    {"q": "Which of these statements about user-defined functions (UDFs) is true?",
     "opts": ["Fully supported as in PostgreSQL PL/pgSQL", "Limited or not supported in same way as Postgres depending on version", "They are required for CDC", "UDFs are used for range-splitting"],
     "ans": "B"},

    {"q": "If a transaction encounters a write-write conflict, CockroachDB will typically:",
     "opts": ["Automatically retry the transaction or return a retryable error to client", "Abort cluster", "Lock the entire table", "Wait indefinitely"],
     "ans": "A"},

    {"q": "Which is true about testing with the Cockroach Simulator?",
     "opts": ["It can't simulate network partitions", "It can simulate latency, partitions, restarts and failures", "It only simulates read queries", "Simulator produces production-ready performance metrics only"],
     "ans": "B"},

    {"q": "Which of the following aids in debugging SQL performance?",
     "opts": ["EXPLAIN (DISTSQL) and EXPLAIN ANALYZE", "Only monitoring UI", "Dropping indexes", "Turning off distributed SQL"],
     "ans": "A"},

    {"q": "What is a good partitioning strategy for multi-tenant workloads?",
     "opts": ["Single table with tenant_id as prefix in primary key to localize tenant data", "Put all tenants in one sequential key space", "Create a separate cluster per tenant always", "Use no partitioning"],
     "ans": "A"},

    {"q": "Which of the following statements about transactions and retries is correct?",
     "opts": ["Clients should implement retry logic for retryable errors", "CockroachDB silently retries everything and clients need do nothing", "All transactions are guaranteed to succeed without retries", "Retrying is never necessary"],
     "ans": "A"},

    {"q": "To reduce cross-region write latency, you might:",
     "opts": ["Move all replicas to a single far region", "Use geo-partitioning and place leaseholders close to clients", "Increase range size", "Disable replication"],
     "ans": "B"},

    {"q": "Which of these is NOT a CockroachDB admin responsibility?",
     "opts": ["Monitoring cluster health", "Designing SQL schemas to avoid contention", "Implementing application-level retry logic", "Writing Raft protocol"],
     "ans": "D"},

    {"q": "When exporting/importing large datasets, what is recommended?",
     "opts": ["Use IMPORT/EXPORT and external storage sinks like S3", "Insert row-by-row via SQL only", "Use single-node dump", "Disable replication during import"],
     "ans": "A"},

    {"q": "What is the main difference between CockroachDB OSS and Enterprise (historically)?",
     "opts": ["Enterprise had additional enterprise-only features like advanced backup/restore and RBAC in earlier versions", "OSS was closed-source", "Enterprise had no support for SQL", "No differences"],
     "ans": "A"},

    {"q": "Which maintenance operation helps reclaim disk space from deleted data?",
     "opts": ["GC (garbage collection)", "Range split", "Scatter", "Add replica"],
     "ans": "A"},

    {"q": "Which API or view gives you insight into replica distribution?",
     "opts": ["SHOW RANGES FROM", "crdb_internal and admin UI range views", "SELECT * FROM ranges", "pg_catalog.replicas"],
     "ans": "B"},

    {"q": "Which of the following is a typical symptom of network partition between nodes?",
     "opts": ["Increased leader elections and elevated latency/errors", "Lower CPU usage", "More range splits", "Fewer leases"],
     "ans": "A"},

    {"q": "What is the appropriate response to a replica mismatch detected by consistency checks?",
     "opts": ["Ignore it", "Run consistency checks and consider recovering or rebalancing the replica", "Delete the replica manually", "Increase range size"],
     "ans": "B"},

    {"q": "Which of these best describes a 'split at' operation?",
     "opts": ["Splitting a range at a specific key boundary", "Merging two ranges", "Deleting a range", "Adding replicas to a range"],
     "ans": "A"},

    {"q": "Which of these is true about ephemeral ports and the cockroach node?",
     "opts": ["Cockroach requires fixed ports only", "Cockroach can be configured with specific ports for SQL and HTTP via flags", "It only uses DNS names", "Ports cannot be changed once started"],
     "ans": "B"},

    {"q": "When designing for heavy analytical queries, which is recommended?",
     "opts": ["Mix OLTP and heavy OLAP on same ranges without planning", "Consider separating workloads, tuning indexes and pushing down execution", "Disable distributed SQL", "Use sequential primary keys only"],
     "ans": "B"},

    {"q": "Which statement accurately reflects CockroachDB's approach to compatibility?",
     "opts": ["CockroachDB is wire-compatible with PostgreSQL in many cases, but not 100%", "Completely identical to MySQL wire protocol", "No SQL compatibility", "Only supports a proprietary SQL dialect"],
     "ans": "A"},

    {"q": "What does the " + "EXPLAIN (DISTSQL)" + " statement show?",
     "opts": ["How queries are planned and whether distributed SQL is used", "Replication status", "Range layout", "Index definitions"],
     "ans": "A"},

    {"q": "How should sensitive credentials (like cloud credentials for backup) be stored?",
     "opts": ["Hardcoded in the app", "Stored securely in environment variables or secret managers and passed to the cluster", "Uploaded to public buckets", "Embedded in SQL script"],
     "ans": "B"},

    {"q": "Which operation may be used to reduce the size of SSTables/levels?",
     "opts": ["Forcing compaction via debug/engine APIs or maintenance windows", "Running VACUUM", "Dropping the cluster", "Turning off replication"],
     "ans": "A"},

    {"q": "Which monitoring approach is recommended for production CockroachDB?",
     "opts": ["Only rely on the admin UI occasionally", "Use Prometheus + Grafana with the metrics exposed by CockroachDB", "No monitoring required", "Use logs only"],
     "ans": "B"},

    {"q": "If you need to place a leaseholder in a particular region for performance, you would use:",
     "opts": ["Manual SSH only", "Zone configuration with lease preferences", "ALTER LEASE commands", "Change primary key"],
     "ans": "B"},

    {"q": "Which of the following statements about CockroachDB's license and versions is accurate?",
     "opts": ["The project has historically used an open-source core with additional enterprise features", "It has always been fully proprietary", "It is a proprietary fork of PostgreSQL", "No licensing differences existed"],
     "ans": "A"},

    {"q": "Which of these can reduce tail latencies for reads?",
     "opts": ["Putting all replicas far from the clients", "Using lease preferences to serve reads locally and tuning caches", "Increasing range size", "Disabling Raft"],
     "ans": "B"},

    {"q": "What should you check first if cluster gossip is failing?",
     "opts": ["Node disk sizes", "Network connectivity, firewall rules and certificates", "Query optimizer stats", "Range split thresholds"],
     "ans": "B"},

    {"q": "Which of the following is a valid reason to manually trigger a scatter?",
     "opts": ["To degrade performance", "To help balance newly split ranges across stores", "To merge ranges", "To remove replicas"],
     "ans": "B"},

    {"q": "What does MVCC stand for and why is it used?",
     "opts": ["Multi-Version Concurrency Control, used for snapshot reads and historical versions", "Multiple Volume Cluster Control, used for storage", "Multi-Value Column Control, used for indexes", "Metadata Version Control, used for schema"],
     "ans": "A"},

    {"q": "What is the simplest way to run a quick single-node CockroachDB for development?",
     "opts": ["cockroach start --insecure --store=store --listen-addr=localhost", "cockroach run dev", "docker run cockroachdb/simple", "cockroach faststart"],
     "ans": "A"},

    {"q": "Which of the following is true about telemetry and reporting?",
     "opts": ["CockroachDB never collects any anonymous telemetry", "Historically optional telemetry could be collected; check current settings and privacy policy", "Telemetry is mandatory and cannot be disabled", "Telemetry contains full user data by default"],
     "ans": "B"},

    {"q": "CockroachDB's cost-based optimizer relies on which of the following?",
     "opts": ["Table statistics and histograms via SHOW STATISTICS and ANALYZE", "Only heuristics with no stats", "Manual query plans", "Index-only statistics"],
     "ans": "A"},

    {"q": "Which operation can be used to move ranges away from a node being decommissioned?",
     "opts": ["Decommission will relocate replicas to other nodes", "Delete node directory", "Stop the cluster", "Manually copy files"],
     "ans": "A"},

    {"q": "What is a good practice when performing a major version upgrade?",
     "opts": ["Skip release notes", "Test upgrades in staging and read upgrade docs carefully", "Upgrade production immediately during peak hours", "Disable backups"],
     "ans": "B"},

    {"q": "Which of these is NOT a valid way to interact with CockroachDB?",
     "opts": ["psql (Postgres client) connecting to SQL port", "The cockroach SQL shell", "REST API for SQL queries", "Admin UI and HTTP endpoints for metrics"],
     "ans": "C"},

    {"q": "CockroachDB's approach to failover is best described as:",
     "opts": ["Manual failover only", "Automatic via consensus and replica reassignment", "Requires leader election by humans", "No failover supported"],
     "ans": "B"},

    {"q": "Which is true about node certificates in secure clusters?",
     "opts": ["Certificates are optional in secure mode", "Nodes use TLS certificates to authenticate and encrypt traffic", "Certificates are not used at all", "Only client certs matter"],
     "ans": "B"},

    {"q": "If you need to limit node resource usage for testing, you might use:",
     "opts": ["OS-level cgroups/containers or instance size limits", "Change zone configs", "Alter range size", "Turn off replication"],
     "ans": "A"},

    {"q": "Which statement about long-running SQL transactions is true?",
     "opts": ["They have no impact on GC and can be ignored", "Long-running transactions can hold intents and delay GC, impacting disk usage", "They speed up compactions", "They reduce contention always"],
     "ans": "B"},

    {"q": "Which of the following is a helpful diagnostic when investigating a slow replica?",
     "opts": ["node logs, Raft metrics, and store-level metrics", "Only checking SQL queries", "Dropping the replica immediately", "Increasing client timeouts only"],
     "ans": "A"},

    {"q": "What is the effect of increasing the replication factor without adding nodes?",
     "opts": ["No change", "More replicas on the same nodes, increasing resource usage and potentially reducing availability", "Instant performance improvement", "Ranges will split more frequently"],
     "ans": "B"},

    {"q": "Which of the following best describes CockroachDB's multi-active availability model?",
     "opts": ["Single writable master per cluster", "Any node can accept reads/writes while consensus ensures correctness", "Only one region can accept writes", "Writes are queued centrally"],
     "ans": "B"},

    {"q": "Why are schema changes in CockroachDB designed to be online?",
     "opts": ["To require cluster downtime", "To allow applications to continue running during migrations", "To force manual backfills", "To disable transactions temporarily"],
     "ans": "B"},

    {"q": "What does 'scrub' (or data consistency checking) help detect?",
     "opts": ["Client errors", "Replica inconsistencies and corruption", "Slow queries only", "Zone config errors only"],
     "ans": "B"},

    {"q": "Which practice helps avoid range imbalance after bulk import?",
     "opts": ["Import into one node only", "Use IMPORT which creates bulk SSTs and then run scatter/split to distribute data", "Disable replication during import", "Use single large transaction for all data"],
     "ans": "B"},

    {"q": "What is the site of truth for cluster configuration and metadata?",
     "opts": ["External config files only", "The cluster's replicated key-value store itself (meta ranges)", "A single master node's local disk", "Cloud provider metadata only"],
     "ans": "B"},

    {"q": "Which of these statements about indexes and zone configs is true?",
     "opts": ["Zone configs can influence where data (including indexes) lives by range constraints", "Zone configs only affect backups", "Indexes ignore zone configs", "Zone configs are deprecated"],
     "ans": "A"},

    {"q": "What is the recommended initial replica placement for most clusters?",
     "opts": ["Single replica per range", "Three replicas across failure domains (3-way replication)", "Five replicas per range always", "Replicas only in one host"],
     "ans": "B"},

    {"q": "Which of the following can help when you detect high Write amplification?",
     "opts": ["Tune compaction and engine settings and review workload patterns", "Increase the number of replicas", "Disable range splitting", "Decrease range target size to tiny values"],
     "ans": "A"},

    {"q": "Which of the following is NOT typically a CockroachDB simulator test?",
     "opts": ["Network partitions", "Node restarts", "UI styling tests", "High latency simulations"],
     "ans": "C"},

    {"q": "How does CockroachDB handle schema versions across nodes?",
     "opts": ["Schema changes are coordinated and tracked in the cluster's metadata and run in a compatible way across nodes", "Schemas are local to each node only", "Manual sync required", "No schema management provided"],
     "ans": "A"},

    {"q": "Which of these is a safe way to decommission a node?",
     "opts": ["Stop the node abruptly and delete store", "Use cockroach node decommission to move replicas off and reconfigure", "Drop all databases then stop node", "Remove node from network"],
     "ans": "B"},

    {"q": "What is the correct scoring rule in this quiz app?",
     "opts": ["+1 per correct, -1 per wrong", "+10 for correct, 0 for wrong", "+100 for correct, -50 for wrong", "Only percentage shown, no points"],
     "ans": "B"},

]

# Ensure we have 100 questions: if not, repeat/extend simple variants to reach 100
if len(QUESTIONS) < 100:
    base = len(QUESTIONS)
    i = 0
    # create additional questions by rephrasing common concepts
    extras = [
        ("What command lists the ranges and their leaseholders?", ["cockroach ranges", "cockroach debug ranges", "SHOW RANGES", "crdb_ranges"], "B"),
        ("Which setting controls the target range size?", ["sql.range.size", "kv.range_size.target", "kv.range.max_bytes", "range.target.size"], "C"),
        ("What is a consequence of having very large ranges?", ["Fewer splits and potential hotspots", "More Raft leaders", "Reduced disk usage always", "Automatic compaction disabled"], "A"),
        ("Which operation helps when a node is slow due to bad disk?", ["Replace the node/store and rebalance replicas", "Increase SQL timeouts only", "Change primary keys", "Disable replication"], "A"),
        ("Which SQL statement can show current sessions?", ["SHOW SESSIONS", "SELECT * FROM pg_stat_activity", "SHOW CLUSTER SESSIONS", "cockroach sessions"], "A"),
        ("Which of the following can be used to enforce locality-aware replica placement?", ["Zone configs with constraints", "Manual SSH placement", "SQL GRANT", "ALTER RANGE PLACEMENT"], "A"),
        ("What tool would you use to simulate workload for benchmarking?", ["workload (cockroach workload)", "pgbench only", "mysqlslap only", "admin UI only"], "A"),
        ("Which of these is a reason to enable lease preferences?", ["To have leaseholders in preferred locations to reduce latency", "To disable replication", "To increase range size", "To merge ranges"], "A"),
        ("Which API can give detailed per-range metrics?", ["admin UI endpoints and crdb_internal tables", "REST API only", "No such API", "pg_catalog only"], "A"),
        ("What is a safe approach to test failure scenarios?", ["Use the cockroach simulator or staging cluster to inject faults", "Test directly in production without backups", "Only simulate by reading docs", "Manually deleting files in prod"], "A"),
    ]
    while len(QUESTIONS) < 100:
        tpl = extras[i % len(extras)]
        QUESTIONS.append({"q": tpl[0] + f" (extra {i})", "opts": tpl[1], "ans": tpl[2]})
        i += 1

# Build mapping for letters
LETTER_MAP = {"A": 0, "B": 1, "C": 2, "D": 3}

st.set_page_config(page_title="CockroachDB Simulator Quiz (100 Q)", layout="wide")
st.title("CockroachDB Simulator — 100-question MCQ Quiz")
st.markdown("**Scoring:** +10 for each correct answer; 0 for each wrong answer.")
st.markdown(f"### Question {idx+1}")
            st.write("Answer all questions and press **Submit**. After submission you'll see which answers were correct or wrong and your total score.")

# Use a form to collect answers and submit once
with st.form(key='quiz_form'):
    st.header("Questions")
    answers = {}
    cols = st.columns(2)
    for idx, item in enumerate(QUESTIONS):
        col = cols[idx % 2]
        qkey = f"q_{idx}"
        opts = item['opts']
        # Build display label combining choices
        answer = col.radio(f"{idx+1}. {item['q']}", options=[f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"], key=qkey)
        answers[qkey] = answer
    submitted = st.form_submit_button("Submit")

if submitted:
    # Calculate score
    total_points = 0
    correct_count = 0
    wrong_count = 0
    st.header("Results")
    for idx, item in enumerate(QUESTIONS):
        qkey = f"q_{idx}"
        selected = st.session_state.get(qkey)
        # selected is like 'A. ...' so take the first letter
        selected_letter = selected[0] if selected else None
        correct_letter = item['ans']
        correct_idx = LETTER_MAP[correct_letter]
        correct_text = item['opts'][correct_idx]

        if selected_letter == correct_letter:
            total_points += 10
            correct_count += 1
            st.success(f"{idx+1}. Correct — You answered {selected_letter}. {selected[3:]} \n**Correct answer:** {correct_letter}. {correct_text}")
        else:
            wrong_count += 1
            st.error(f"{idx+1}. Wrong — You answered {selected_letter if selected_letter else 'No answer'}. {selected[3:] if selected else ''} \n**Correct answer:** {correct_letter}. {correct_text}")

    st.markdown(f"### Summary\n- Total questions: {len(QUESTIONS)}\n- Correct: {correct_count}\n- Wrong: {wrong_count}\n- **Score: {total_points} / {len(QUESTIONS)*10}**")

    # Option to show only incorrect for review
    if st.button("Show only incorrect questions for review"):
        st.header("Incorrect Questions")
        for idx, item in enumerate(QUESTIONS):
            qkey = f"q_{idx}"
            selected = st.session_state.get(qkey)
            selected_letter = selected[0] if selected else None
            if selected_letter != item['ans']:
                correct_letter = item['ans']
                correct_idx = LETTER_MAP[correct_letter]
                correct_text = item['opts'][correct_idx]
                st.write(f"{idx+1}. {item['q']}")
                st.write(f"Your answer: {selected_letter if selected_letter else 'No answer'} — {selected[3:] if selected else ''}")
                st.write(f"Correct: {correct_letter} — {correct_text}")
                st.markdown("---")

    st.balloons()

else:
    st.info("When you finish answering all questions, press Submit to see your score and detailed feedback.")

# Footer
st.markdown("---")
st.write("Generated CockroachDB Simulator quiz app. Modify QUESTIONS to change or update questions/answers.")
