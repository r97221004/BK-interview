"""Question data for the backend interview question set.

Each part owns a block of numbers (1-9, 11-19, 21-29, ...) so a new question can
be added to a part without renumbering everything after it. Numbers are
permanent: links and bookmarks must keep pointing at the same question, which is
why a part that fills its block takes a fresh one rather than pushing its
neighbours along - see "API Design & Reliability" at 61.

Each entry: num, dir, slug, title, focus, tests.
  focus - the one-line "Focus" cell in the README table
  tests - the blockquote under the title: what the interviewer is really asking
"""

# Display order. A part's number block is its permanent identity and has nothing
# to do with where it appears here, which is why "API Design & Reliability" reads
# second but numbers from 61: it was added after the 1-9 block was already full,
# and renumbering the questions above it would have broken every existing link.
PARTS = [
    ("api-and-http", "API & HTTP"),
    ("api-design", "API Design & Reliability"),
    ("databases", "Databases"),
    ("security-and-auth", "Security & Auth"),
    ("architecture-and-scaling", "Architecture & Scaling"),
    ("devops-and-deployment", "DevOps & Deployment"),
    ("testing-and-debugging", "Testing & Debugging"),
]

Q = []


def q(num, d, slug, title, focus, tests):
    Q.append(dict(num=num, dir=d, slug=slug, title=title, focus=focus, tests=tests))


# ------------------------------------------------------------- API & HTTP
q(1, "api-and-http", "what-is-a-restful-api",
  "What is a RESTful API, and what are its core principles?",
  "The six constraints, and which ones actually change your design",
  "Tests whether you can name REST's constraints and explain what each one buys you, instead of equating REST with 'JSON over HTTP'.")

q(2, "api-and-http", "http-request-response-cycle",
  "Can you describe a typical HTTP request/response cycle?",
  "Connection, request, processing, response, and connection reuse",
  "Tests whether you can follow a request end to end, including the TCP connection underneath and what persistent connections changed.")

q(3, "api-and-http", "what-is-an-api-endpoint",
  "What is an API endpoint?",
  "A URL as the entry point to one resource or capability",
  "Usually an opener. Tests whether you can define the term precisely and connect it to how a server routes work.")

q(4, "api-and-http", "http-statelessness",
  "Explain statelessness in HTTP and how it impacts backend services.",
  "Independent requests, and where the state has to go instead",
  "Tests whether you understand that statelessness is a protocol property that pushes state management into your design, not a claim that applications have no state.")

q(5, "api-and-http", "rest-benefits-and-drawbacks",
  "What are the benefits and drawbacks of RESTful APIs?",
  "Scalability and standardization vs over-fetching and versioning cost",
  "Tests whether you can criticize the style you use daily, and name the cases where REST is the wrong tool.")

q(6, "api-and-http", "api-versioning",
  "How do you approach API versioning in your projects?",
  "URL vs header versioning, and when a version is needed at all",
  "Tests whether you can change a live API without breaking clients, and whether you know versioning is a cost to be avoided when possible.")

q(7, "api-and-http", "securing-a-new-api",
  "What measures would you take to secure a newly developed API?",
  "Identity, permission, input, protection, monitoring - as five layers",
  "Tests whether you can give a structure an interviewer can dig into, rather than reciting security keywords. Authorization is the layer that separates the two.")

q(8, "api-and-http", "rest-vs-websocket",
  "What is the difference between a REST API and a WebSocket?",
  "Request-response vs a persistent bidirectional connection",
  "Tests whether you can name the cases that actually need server push, and what a long-lived connection costs the backend.")

q(9, "api-and-http", "file-uploads",
  "How would you handle file uploads in a web application?",
  "Validation, naming, metadata, and keeping bytes out of the app server",
  "Tests whether you treat uploads as untrusted input and whether you know the scaling problem hidden in the naive implementation.")

q(10, "api-and-http", "tcp-vs-udp",
  "What is the difference between TCP and UDP?",
  "A reliable ordered stream vs fire-and-forget datagrams, and what the guarantee costs",
  "Tests whether you can get past 'TCP is reliable, UDP is fast' to what the reliability actually costs - a round trip before any data moves, and one lost packet stalling everything behind it.")

# ------------------------------------------------------------- Databases
q(11, "databases", "sql-vs-nosql",
  "Can you explain the difference between SQL and NoSQL databases?",
  "Relational schema and ACID vs flexible models and horizontal scale",
  "Tests whether you can choose between them for a stated workload, rather than reciting 'SQL is structured, NoSQL is flexible'.")

q(12, "databases", "data-normalization",
  "What is data normalization?",
  "1NF to BCNF, the anomalies each form removes, and when to stop",
  "Tests whether you can explain the normal forms in terms of the update anomalies they prevent, and whether you know when denormalizing is correct.")

q(13, "databases", "data-partitioning",
  "What is data partitioning?",
  "Horizontal, vertical, range, hash, and list partitioning",
  "Tests whether you can pick a partition key for a stated access pattern, and whether you know what partitioning makes harder.")

q(14, "databases", "redis-use-cases",
  "What are the common application scenarios for Redis?",
  "Cache, session store, rate limiter, queue, and leaderboard",
  "Tests whether you know why an in-memory store is used for these jobs, and what you lose by putting data there.")

q(15, "databases", "database-out-of-storage",
  "What strategies do you have when a database runs out of storage?",
  "Immediate relief, then reclaiming, growing, and splitting",
  "Tests whether you can separate the emergency response from the structural fix, and whether you monitor for this before it happens.")

q(16, "databases", "indexes-and-slow-queries",
  "What is a database index, and how do you work out why a query is slow?",
  "B-tree lookup, what an index costs, and reading a query plan",
  "The highest-value database question there is. Tests whether you can reason from the access path rather than guess, and whether you know an index is not free.")

q(17, "databases", "transactions-and-isolation-levels",
  "Explain database transactions and isolation levels.",
  "ACID in practice, the four levels, and the anomalies each prevents",
  "Tests whether you know what your default isolation level actually allows, and whether you can recognise a deadlock and say what causes one.")

q(18, "databases", "n-plus-one-queries",
  "What is the N+1 query problem, and how do you fix it?",
  "One query per row, why an ORM hides it, and eager loading",
  "Tests whether you can spot the most common performance bug in ORM-backed code, and whether you would have noticed it before production did.")

q(19, "databases", "caching-strategy-and-invalidation",
  "How do you decide what to cache, and how do you invalidate it?",
  "Cache-aside vs write-through, TTLs, stampedes, and staleness",
  "Tests whether you treat caching as a design with failure modes rather than as a switch, and whether you can say what happens on a miss.")

q(20, "databases", "schema-migrations",
  "How do you change a database schema without downtime?",
  "Expand and contract, backwards-compatible steps, and long locks",
  "Tests whether you know a migration runs while the old code is still serving traffic, and whether you have been bitten by a lock on a large table.")

# ------------------------------------------------------------- Security & Auth
q(21, "security-and-auth", "session-vs-jwt-authentication",
  "What is the difference between session-based and JWT-based authentication?",
  "Server-side state vs a signed self-contained token",
  "Tests whether you can trade revocation against statelessness, instead of declaring one of them modern and the other legacy.")

q(22, "security-and-auth", "session-vs-cookie",
  "What is the difference between a session and a cookie?",
  "Client-side storage vs server-side state, and how they connect",
  "Tests whether you can separate the transport mechanism from the state it points at - a common confusion in interviews.")

q(23, "security-and-auth", "sql-injection",
  "How do you protect a server from SQL injection attacks?",
  "Parameterized queries, ORMs, and defense in depth",
  "Tests whether you know that the fix is separating code from data, not filtering bad characters.")

q(24, "security-and-auth", "session-management",
  "Describe how session management works in web applications.",
  "Session lifecycle, storage, and scaling it across servers",
  "Tests whether you can walk the full lifecycle and explain what breaks when a second application server appears.")

q(25, "security-and-auth", "xss",
  "What is Cross-Site Scripting (XSS)?",
  "Injected script running with the trusted site's privileges",
  "Tests whether you know that the fix is context-correct output encoding, and whether you can name the three XSS variants.")

q(26, "security-and-auth", "csrf",
  "What is Cross-Site Request Forgery (CSRF)?",
  "Riding the victim's ambient credentials, and how tokens stop it",
  "Tests whether you can explain why the browser sends the cookie at all, and how CSRF differs from XSS.")

q(27, "security-and-auth", "cors",
  "What is CORS?",
  "Same-origin policy, preflight, and what CORS does not protect",
  "Tests whether you know CORS is a browser rule that relaxes a restriction, not a server-side security control.")

q(28, "security-and-auth", "jwt-hs256-vs-rs256",
  "What is the difference between HS256 and RS256 for signing a JWT?",
  "A shared secret vs a key pair, and why the choice is about who has to verify",
  "Tests whether you pick a signing algorithm from who needs to verify the token rather than from a benchmark, and whether you can explain why an unpinned algorithm is exploitable.")

# ------------------------------------------------- Architecture & Scaling
q(31, "architecture-and-scaling", "scaling-during-traffic-surge",
  "How would you scale a backend application during a traffic surge?",
  "Horizontal scaling, statelessness, caching, and shedding load",
  "Tests whether you can name the bottleneck before the remedy, and whether you know the database is usually the real limit.")

q(32, "architecture-and-scaling", "python-concurrency-models",
  "Discuss multiprocessing, multithreading, and asynchronous I/O in Python.",
  "The GIL, and matching the model to I/O-bound or CPU-bound work",
  "Tests whether you can pick a concurrency model from the workload, and whether you understand what the GIL does and does not block.")

q(33, "architecture-and-scaling", "python-builtin-data-structures",
  "Explain the underlying data structures of lists, sets, tuples, and dictionaries in Python.",
  "Dynamic arrays and hash tables, and the complexity that follows",
  "Tests whether you can derive the performance characteristics from the implementation instead of memorizing a complexity table.")

q(34, "architecture-and-scaling", "maintainable-backend-code",
  "How do you ensure your backend code is maintainable and easy to understand?",
  "Boundaries, conventions, tests, and consistent failure handling",
  "Tests whether you have habits that survive a growing team, rather than a list of style rules.")

q(35, "architecture-and-scaling", "message-queues-and-async-work",
  "When would you move work onto a message queue?",
  "Decoupling, absorbing bursts, and what a queue makes harder",
  "Tests whether you can name work that does not belong in a request cycle, and whether you know a queue introduces retries, ordering, and duplicate delivery.")

q(36, "architecture-and-scaling", "monolith-vs-microservices",
  "Monolith or microservices - how would you decide?",
  "Deployment coupling, team boundaries, and the costs you inherit",
  "Tests whether you can argue for the boring choice. Reciting the benefits of microservices without naming the operational cost is the failure mode.")

q(37, "architecture-and-scaling", "timeouts-retries-and-failure",
  "How do you stop one slow dependency from taking down your service?",
  "Timeouts, bounded retries with backoff, and circuit breakers",
  "Tests whether you treat a network call as something that fails, and whether you know a naive retry turns a blip into an outage.")

q(38, "architecture-and-scaling", "connection-pooling",
  "What is a database connection pool, and how do you size it?",
  "Reusing an expensive connection, and why a bigger pool is not a faster one",
  "Tests whether you know the pool is a limit as much as a reuse mechanism - that the database sets the ceiling, not the application, and that exhausting it looks like a total outage rather than a slow query.")

# ---------------------------------------------------- DevOps & Deployment
q(41, "devops-and-deployment", "what-is-containerization",
  "What is containerization, and how does it benefit backend development?",
  "Packaging the runtime with the app, and the boundary of that promise",
  "Tests whether you can state what containers actually isolate, and what they do not solve.")

q(43, "devops-and-deployment", "zero-downtime-deploys",
  "How do you deploy a new version without dropping requests?",
  "Rolling, blue-green, and canary, plus health checks and rollback",
  "Tests whether you have shipped to production. The revealing part is what you do when the new version is bad, not how you get it out.")

# ---------------------------------------------------- Testing & Debugging
q(51, "testing-and-debugging", "testing-a-new-api-endpoint",
  "What kind of tests would you write for a new API endpoint?",
  "Unit, integration, contract, and load tests, and what each proves",
  "Tests whether you can say what each layer is responsible for, instead of listing test types.")

q(52, "testing-and-debugging", "debugging-a-backend-application",
  "What tools and techniques do you use for debugging a backend application?",
  "Reproduce, narrow, then instrument - locally and in production",
  "Tests whether you have a method rather than a tool list, and whether you can debug something you cannot attach a debugger to.")


# --------------------------------------------- API Design & Reliability
q(61, "api-design", "status-codes-and-error-responses",
  "How do you choose HTTP status codes and design error responses?",
  "Status classes, and an error body a client can act on",
  "Tests whether you design errors for the caller rather than for yourself, and whether you know why returning 200 with an error body breaks clients and proxies.")

q(62, "api-design", "pagination",
  "How would you paginate a large collection endpoint?",
  "Offset vs cursor pagination, and why deep offsets get slow",
  "Tests whether you know offset pagination degrades on large tables and skips rows when the data shifts underneath the reader.")

q(63, "api-design", "idempotency-and-retries",
  "How do you make an endpoint safe to retry?",
  "Idempotent methods, idempotency keys, and exactly-once delivery",
  "Tests whether you have thought about what happens when a client times out and retries a payment - the classic double-charge.")
