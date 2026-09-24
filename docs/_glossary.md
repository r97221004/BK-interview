# Glossary

> The vocabulary the answers assume. Every term links to the question that explains it properly.

Questions link here on first use, so you can read in any order without hitting a term you have not met yet. If backend work is new to you, skimming this once first is worth the five minutes.

### Endpoint

A single URL a server exposes, combined with the HTTP methods it accepts. It is the entry point to one [resource](#resource) or capability, and it is what a router maps to a handler function.

Explained in full: [Q03](api-and-http/q03-what-is-an-api-endpoint.md).

### REST

An architectural style for networked applications, defined by six constraints rather than by a wire format. An API that ignores the constraints is not RESTful just because it returns JSON.

Explained in full: [Q01](api-and-http/q01-what-is-a-restful-api.md).

### Resource

The thing a URL names - a user, an order, a collection of orders. [REST](#rest) models the API as nouns acted on by standard HTTP methods, rather than as remote function calls.

Explained in full: [Q01](api-and-http/q01-what-is-a-restful-api.md).

### Idempotent

A method is idempotent when repeating the same request has the same effect as sending it once. GET, PUT, and DELETE are idempotent; POST is not, which is why retrying a failed POST can double-charge a customer.

Explained in full: [Q63](api-design/q63-idempotency-and-retries.md).

### Statelessness

The rule that each request carries everything the server needs to process it. The server keeps no per-client memory between requests, so any request can be served by any instance.

Explained in full: [Q04](api-and-http/q04-http-statelessness.md).

### Status code

The three-digit result on an HTTP response: 2xx success, 3xx redirect, 4xx the client's fault, 5xx the server's fault. Clients and proxies both branch on this, so returning 200 with an error body breaks them.

Explained in full: [Q61](api-design/q61-status-codes-and-error-responses.md).

### Persistent connection

Reuse of one [TCP](#tcp) connection for several request/response pairs, the default since HTTP/1.1. It removes a handshake per request, which is why [connection pooling](#connection-pool) matters for service-to-service calls.

Explained in full: [Q02](api-and-http/q02-http-request-response-cycle.md).

### TCP

The transport that turns IP's best-effort packets into a reliable, ordered byte stream: it opens a connection with a handshake, numbers every byte, retransmits whatever is not acknowledged, and slows itself down when the network is congested.

Explained in full: [Q10](api-and-http/q10-tcp-vs-udp.md).

### UDP

The transport that adds almost nothing to IP - ports, a length, and a checksum, in eight bytes of header. Each datagram either arrives whole or not at all, with no connection, no retransmission, and no ordering, so recovering from loss is the application's job.

Explained in full: [Q10](api-and-http/q10-tcp-vs-udp.md).

### Head-of-line blocking

One stalled item holding up everything queued behind it, even data that has already arrived. It happens at the HTTP layer when a response blocks the next request on the connection, and at the [TCP](#tcp) layer when one lost packet blocks every stream sharing that connection.

Explained in full: [Q10](api-and-http/q10-tcp-vs-udp.md).

### WebSocket

A protocol that upgrades an HTTP connection into a long-lived, bidirectional channel. Once open, the server can push to the client without being asked, which plain HTTP cannot do.

Explained in full: [Q08](api-and-http/q08-rest-vs-websocket.md).

### API versioning

Serving more than one contract at a time so existing clients keep working while the API evolves. The version can live in the URL path or in a request header.

Explained in full: [Q06](api-and-http/q06-api-versioning.md).

### Breaking change

A change that makes a previously valid client request fail or be misinterpreted: removing a field, renaming one, tightening validation, or changing a [status code](#status-code). Adding an optional field is not one.

Explained in full: [Q06](api-and-http/q06-api-versioning.md).

### Presigned URL

A time-limited URL, signed by the backend, that lets a client upload to or download from object storage directly. It keeps large file bytes out of the application server entirely.

Explained in full: [Q09](api-and-http/q09-file-uploads.md).

### Cookie

A small key-value pair the server asks the browser to store and send back automatically on later requests to that site. It is a transport for state, not the state itself.

Explained in full: [Q22](security-and-auth/q22-session-vs-cookie.md).

### Session

Server-side state belonging to one logged-in client, keyed by a session ID. The client holds only the ID; the data - user, roles, expiry - stays on the server or in a shared store.

Explained in full: [Q24](security-and-auth/q24-session-management.md).

### JWT

A JSON Web Token: a signed, self-describing token carrying claims such as user ID and expiry. Anyone can read it; only the holder of the key can forge one. Signed is not encrypted.

Explained in full: [Q21](security-and-auth/q21-session-vs-jwt-authentication.md).

### HMAC

A keyed hash: a secret is mixed into the hash of the message, so only a holder of that secret can produce or check the result. The same key does both, which is why anyone who can verify an HMAC can also forge one.

Explained in full: [Q28](security-and-auth/q28-jwt-hs256-vs-rs256.md).

### JWKS

A JSON Web Key Set: the document an issuer publishes its public keys at, each with a key ID that signed tokens name in their header. Verifiers fetch the key a token names, so rotating keys needs no redeploy.

Explained in full: [Q28](security-and-auth/q28-jwt-hs256-vs-rs256.md).

### Same-origin policy

The browser rule that scripts on one origin - scheme, host, and port together - cannot read responses from another origin. It is the restriction [CORS](#cors) selectively relaxes.

Explained in full: [Q27](security-and-auth/q27-cors.md).

### CORS

Cross-Origin [Resource](#resource) Sharing: response headers by which a server tells the browser which other origins may read its responses. It is enforced by the browser and applies to nothing else.

Explained in full: [Q27](security-and-auth/q27-cors.md).

### Preflight request

An automatic `OPTIONS` request the browser sends before a cross-origin request that is not simple, asking whether the real request is allowed. The answer is cacheable via `Access-Control-Max-Age`.

Explained in full: [Q27](security-and-auth/q27-cors.md).

### CSRF

Cross-Site Request Forgery: an attacker causes the victim's browser to send a state-changing request to a site where the victim is already authenticated, relying on [cookies](#cookie) being attached automatically.

Explained in full: [Q26](security-and-auth/q26-csrf.md).

### SameSite

A [cookie](#cookie) attribute that tells the browser when to attach the cookie to cross-site requests. `Lax` blocks it on cross-site POSTs, `Strict` blocks it on all cross-site navigation, `None` requires `Secure`.

Explained in full: [Q26](security-and-auth/q26-csrf.md).

### XSS

Cross-Site Scripting: attacker-supplied script executes in another user's browser with the victim site's origin and privileges, so it can read the DOM and any token reachable from JavaScript.

Explained in full: [Q25](security-and-auth/q25-xss.md).

### Content Security Policy

A response header restricting which script, style, and connection sources a page may use. It is a second line of defense that limits the damage of an injection you failed to escape.

Explained in full: [Q25](security-and-auth/q25-xss.md).

### Output encoding

Escaping data for the exact context it is rendered into - HTML body, attribute, JavaScript literal, URL. The correct escaping differs per context, which is why one global sanitize step is not enough.

Explained in full: [Q25](security-and-auth/q25-xss.md).

### SQL injection

An attack where user input is concatenated into a query and changes its structure rather than only supplying values. The fix is to send the query and the data to the database separately.

Explained in full: [Q23](security-and-auth/q23-sql-injection.md).

### Prepared statement

A query sent to the database with placeholders, followed by the values. The database parses the query before it sees the data, so input can never become part of the command.

Explained in full: [Q23](security-and-auth/q23-sql-injection.md).

### ORM

Object-Relational Mapping: a library that generates SQL from objects and method calls. It uses [prepared statements](#prepared-statement) by default, which is why it removes most injection risk incidentally.

Explained in full: [Q23](security-and-auth/q23-sql-injection.md).

### Least privilege

Granting an account only the permissions its job requires. An application database user that cannot `DROP` limits what any successful injection can actually do.

Explained in full: [Q23](security-and-auth/q23-sql-injection.md).

### ACID

Atomicity, Consistency, Isolation, Durability: the transactional guarantees relational databases provide. They are what let you move money between two rows without inventing or losing any.

Explained in full: [Q17](databases/q17-transactions-and-isolation-levels.md).

### Normalization

Organizing tables so each fact is stored exactly once, removing the insert, update, and delete anomalies that duplicated data causes.

Explained in full: [Q12](databases/q12-data-normalization.md).

### Denormalization

Deliberately duplicating data to avoid a join on a read-heavy path. It trades write complexity and the risk of divergence for read speed, and is a decision, not an accident.

Explained in full: [Q12](databases/q12-data-normalization.md).

### Partitioning

Splitting one logical table into smaller physical pieces so a query touches only the relevant piece. Vertical splits columns; horizontal splits rows by range, hash, or list.

Explained in full: [Q13](databases/q13-data-partitioning.md).

### Sharding

Horizontal [partitioning](#partitioning) across separate database servers. It is the only way to scale writes past one machine, and it makes cross-shard joins and transactions expensive or impossible.

Explained in full: [Q13](databases/q13-data-partitioning.md).

### Index

A secondary structure, usually a B-tree, that lets the database find rows without scanning the table. Each index speeds up reads and slows down every write to that table, and consumes disk.

Explained in full: [Q16](databases/q16-indexes-and-slow-queries.md).

### Cache

A fast store holding a copy of data that is expensive to recompute or refetch. Every cache needs an answer for how entries expire and what happens on a miss.

Explained in full: [Q19](databases/q19-caching-strategy-and-invalidation.md).

### Redis

An in-memory data-structure store used as a [cache](#cache), [session](#session) store, [rate limit](#rate-limiting)er, and [queue](#message-queue). Its speed comes from keeping data in RAM, which is also why capacity and durability need explicit thought.

Explained in full: [Q14](databases/q14-redis-use-cases.md).

### Horizontal scaling

Adding more instances behind a [load balancer](#load-balancer), as opposed to vertical scaling, which makes one machine bigger. It requires the instances to be interchangeable.

Explained in full: [Q31](architecture-and-scaling/q31-scaling-during-traffic-surge.md).

### Load balancer

The component distributing incoming requests across instances. It also health-checks them, which is how a failing instance stops receiving traffic.

Explained in full: [Q31](architecture-and-scaling/q31-scaling-during-traffic-surge.md).

### CDN

A network of edge [caches](#cache) serving static assets close to the user. It removes the largest and dullest slice of traffic from your origin before it ever arrives.

Explained in full: [Q31](architecture-and-scaling/q31-scaling-during-traffic-surge.md).

### Backpressure

Deliberately rejecting or queueing work when the system is saturated, so it degrades instead of collapsing. [Rate limits](#rate-limiting), [queue](#message-queue) bounds, and load shedding are all forms of it.

Explained in full: [Q31](architecture-and-scaling/q31-scaling-during-traffic-surge.md).

### GIL

CPython's Global Interpreter Lock: only one thread executes Python bytecode at a time. It blocks CPU-bound parallelism in threads, but is released during I/O, which is why threads still help there.

Explained in full: [Q32](architecture-and-scaling/q32-python-concurrency-models.md).

### Event loop

The single-threaded scheduler behind `asyncio`. It runs a task until the task yields with `await`, then runs another, so one blocking call stalls everything.

Explained in full: [Q32](architecture-and-scaling/q32-python-concurrency-models.md).

### Hash table

The structure behind `dict` and `set`: a key is hashed to an [index](#index) into an array of slots, giving average O(1) lookup. Collisions are resolved by probing, and the table resizes as it fills.

Explained in full: [Q33](architecture-and-scaling/q33-python-builtin-data-structures.md).

### Dynamic array

The structure behind `list`: a contiguous block of references that is over-allocated and copied to a larger block when it fills, giving amortized O(1) append and O(n) insertion in the middle.

Explained in full: [Q33](architecture-and-scaling/q33-python-builtin-data-structures.md).

### Containerization

Packaging an application with its runtime, libraries, and configuration into an image that runs the same everywhere, isolated by kernel namespaces and cgroups rather than by a hypervisor.

Explained in full: [Q41](devops-and-deployment/q41-what-is-containerization.md).

### Unit test

A test of one unit of behavior through its public interface, with no database, network, or filesystem. Fast and precise about where the failure is.

Explained in full: [Q51](testing-and-debugging/q51-testing-a-new-api-endpoint.md).

### Integration test

A test that exercises the real [endpoint](#endpoint) over HTTP against real dependencies, proving the wiring works. Slower, and the thing that catches what [unit tests](#unit-test) mocked away.

Explained in full: [Q51](testing-and-debugging/q51-testing-a-new-api-endpoint.md).

### Structured logging

Emitting logs as key-value records rather than prose, so they can be filtered and aggregated. A request ID on every line is what makes one request traceable across services.

Explained in full: [Q52](testing-and-debugging/q52-debugging-a-backend-application.md).

### Observability

Being able to answer new questions about a running system without shipping new code, using logs, metrics, and traces together.

Explained in full: [Q52](testing-and-debugging/q52-debugging-a-backend-application.md).

### TLS

The encryption layer under HTTPS. It protects data in transit from being read or modified, and authenticates the server. It says nothing about who the caller is.

Explained in full: [Q07](api-and-http/q07-securing-a-new-api.md).

### Rate limiting

Capping how many requests a caller may make in a window, to contain abuse, scraping, and accidental retry storms. Usually keyed by API key, user, or IP.

Explained in full: [Q07](api-and-http/q07-securing-a-new-api.md).

### OAuth 2.0

A delegation framework that lets a third party act on a user's behalf without receiving their password. It is authorization, not authentication - that is what OpenID Connect adds.

Explained in full: [Q07](api-and-http/q07-securing-a-new-api.md).

### Query plan

What the database decided to do with your query - which [index](#index), which join order, in what sequence. `EXPLAIN` prints it, and `EXPLAIN ANALYZE` adds the timings and the row counts it actually saw.

Explained in full: [Q16](databases/q16-indexes-and-slow-queries.md).

### Deadlock

Two transactions each holding a lock the other needs, so neither can move. The database detects the cycle and aborts one of them, which reaches your application as an error on a statement that was correct.

Explained in full: [Q17](databases/q17-transactions-and-isolation-levels.md).

### N+1 query

One query to fetch a list, then one more per item in it. The application code shows no query at all, because the [ORM](#orm) issues it lazily behind an attribute access.

Explained in full: [Q18](databases/q18-n-plus-one-queries.md).

### Cache-aside

The usual [caching](#cache) pattern: check the cache, and on a miss read the source, write the value back with an expiry, and return it. The cache never talks to the database itself, so losing it costs speed rather than correctness.

Explained in full: [Q19](databases/q19-caching-strategy-and-invalidation.md).

### Cache stampede

A popular key expires and every concurrent request misses at once, so the whole load arrives at the database together. Prevented with a short lock on repopulation, or by adding random jitter to expiry times.

Explained in full: [Q19](databases/q19-caching-strategy-and-invalidation.md).

### Cursor pagination

Paging by sending a pointer to the last row seen rather than a page number, so the query seeks the [index](#index) directly. Constant cost at any depth, and immune to rows shifting under the reader.

Explained in full: [Q62](api-design/q62-pagination.md).

### Idempotency key

A unique value the client generates once per logical operation and reuses across retries. The server records it with the result, so a repeat returns the original response instead of doing the work twice.

Explained in full: [Q63](api-design/q63-idempotency-and-retries.md).

### At-least-once delivery

The guarantee you actually get over an unreliable network or from a [queue](#message-queue): a message may arrive more than once, never fewer. Exactly-once processing is achieved in the handler, not in the transport.

Explained in full: [Q63](api-design/q63-idempotency-and-retries.md).

### Message queue

A buffer between a producer and a worker, so slow work leaves the request cycle and a traffic spike becomes a backlog that drains instead of a wall of [timeouts](#timeout).

Explained in full: [Q35](architecture-and-scaling/q35-message-queues-and-async-work.md).

### Dead-letter queue

Where a job goes after it has failed its retries, so it stops blocking the [queue](#message-queue) and can be inspected instead of silently disappearing.

Explained in full: [Q35](architecture-and-scaling/q35-message-queues-and-async-work.md).

### Schema migration

A versioned, reviewed change to the database structure, applied by a tool that tracks what has already run. It executes while the previous version of the application is still serving traffic.

Explained in full: [Q20](databases/q20-schema-migrations.md).

### Expand and contract

Making a schema change in additive steps first - add, dual-write, backfill, switch reads - and only removing the old shape in a later deploy, so old and new code are both valid at every point.

Explained in full: [Q20](databases/q20-schema-migrations.md).

### Microservices

An architecture of many independently deployable services. It buys independent release and scaling, and charges for it by turning every internal call into a network call that can fail.

Explained in full: [Q36](architecture-and-scaling/q36-monolith-vs-microservices.md).

### Timeout

A deadline on an outbound call. Without one, a slow dependency does not fail - it holds your worker until the pool is empty, which is how one slow service takes down another.

Explained in full: [Q37](architecture-and-scaling/q37-timeouts-retries-and-failure.md).

### Connection pool

A fixed set of open database connections the application borrows from and returns to, instead of opening one per query. It exists as much to cap how many connections reach the database as to save the handshake, because the database, not the application, decides how many it can usefully serve.

Explained in full: [Q38](architecture-and-scaling/q38-connection-pooling.md).

### Circuit breaker

A guard that watches the failure rate of a dependency and, past a threshold, fails calls immediately without attempting them. It frees your workers and gives the failing service room to recover.

Explained in full: [Q37](architecture-and-scaling/q37-timeouts-retries-and-failure.md).

### Health check

The [endpoint](#endpoint) a [load balancer](#load-balancer) or orchestrator polls to decide whether an instance should receive traffic. Liveness means the process is alive; readiness means it can actually serve.

Explained in full: [Q43](devops-and-deployment/q43-zero-downtime-deploys.md).

### Blue-green deploy

Running a complete second environment on the new version and switching all traffic at once. Cutover and rollback are both instant, at the cost of double infrastructure during the switch.

Explained in full: [Q43](devops-and-deployment/q43-zero-downtime-deploys.md).

### Canary deploy

Sending a small, increasing share of real traffic to the new version while comparing its error rate and latency against the old one, so a bad release reaches few users.

Explained in full: [Q43](devops-and-deployment/q43-zero-downtime-deploys.md).

### IDOR

Insecure Direct Object Reference, also called broken object level authorization: the caller is authenticated, but the handler trusts the identifier in the request and returns or edits a record belonging to someone else. First in the OWASP API Security Top 10.

Explained in full: [Q07](api-and-http/q07-securing-a-new-api.md).

### Mass assignment

Binding a request payload straight onto a model, so a caller can set a field the API never meant to expose - a role or an ownership column. The fix is an explicit input schema, and an explicit output schema so internal fields cannot ride along either.

Explained in full: [Q07](api-and-http/q07-securing-a-new-api.md).
