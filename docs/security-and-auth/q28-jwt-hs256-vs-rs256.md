# Q28: What is the difference between HS256 and RS256 for signing a JWT?

> Tests whether you pick a signing algorithm from who needs to verify the token rather than from a benchmark, and whether you can explain why an unpinned algorithm is exploitable.

**Part:** Security & Auth | **Importance:** 7/10 | **Status:** Complete

**New to these terms?** [endpoint](../_glossary.md#endpoint), [jwt](../_glossary.md#jwt)

## In One Sentence

HS256 signs the token with a single shared secret that both signs and checks, while RS256 signs it with a private key only the issuer holds and checks it with a public key anyone is allowed to have.

HS256 用一把共用的密鑰簽章，簽和驗都是同一把；RS256 則用只有發行者持有的私鑰簽章，再用任何人都可以取得的公鑰來驗證。

## Answer Shape

Define each in a line - a shared secret against a key pair - then go straight to the decision rule, because that is the real question: who has to verify this token? If the service issuing it is the only one that checks it, HS256 is enough. The moment anyone else verifies, HS256 hands them the ability to mint tokens too, and removing that is the entire point of RS256. Finish on the algorithm-confusion attack, because it is the reason the verifier must decide the algorithm instead of reading it out of the token.

先各用一句話定義 —— 一把共用密鑰，對上一組金鑰對 —— 然後直接進到判斷準則，因為真正的問題是：誰需要驗證這個 token？如果只有簽發它的服務會驗，HS256 就夠了。但只要有第二方要驗，HS256 等於同時把簽發 token 的能力交出去，而拿掉這件事正是 RS256 的全部意義。最後收在 algorithm confusion 攻擊，因為那就是驗證端必須自己決定演算法、而不是從 token 裡讀出來的理由。

## Full Spoken Answer

Both produce a token with the same three-part shape, and the only thing that differs is how the third part is computed. HS256 is HMAC with SHA-256: a secret is mixed into the hash of the header and payload, and verifying means recomputing that same value with that same secret and comparing. RS256 is an RSA signature over a SHA-256 digest: the issuer signs with a private key, and the verifier checks it with the matching public key, which cannot produce a signature of its own. So HS256 is symmetric, one key on both sides, and RS256 is asymmetric.

兩者產出的 token 形狀完全一樣，都是三段，差別只在第三段怎麼算出來。HS256 是 HMAC 搭配 SHA-256：把一把密鑰混進標頭與 payload 的雜湊裡，驗證就是用同一把密鑰重算一次同樣的值再比對。RS256 則是對 SHA-256 摘要做 RSA 簽章：發行者用私鑰簽，驗證端用對應的公鑰檢查，而公鑰本身產不出任何簽章。所以 HS256 是對稱式，兩邊用同一把鑰匙；RS256 是非對稱式。

That difference is the whole decision, and the question I would ask out loud is who has to verify. Under HS256 the verification key is the signing key, so every service able to check a token is equally able to issue one. Inside a single service that signs and verifies its own tokens that is fine, and HS256 is the simpler choice: one secret, no key distribution. But the moment a second party verifies - another service, a mobile client, a partner - you have handed each of them the power to mint a token for any user, including an administrator. RS256 removes that: the private key never leaves the issuer, the public key is published, and a verifier can check every token while being unable to forge a single one.

這個差別就決定了一切，而我會把這個問題講出來：誰需要驗證？在 HS256 底下，驗證用的鑰匙就是簽章用的鑰匙，所以每一個能檢查 token 的服務，也同樣能簽發 token。如果簽發與驗證都發生在同一個服務裡，這沒有問題，HS256 還比較簡單：一把密鑰，不必配送金鑰。但只要有第二方要驗 —— 另一個服務、行動端、合作夥伴 —— 你就等於把「替任何使用者簽出 token」的能力一併交了出去，包括管理員。RS256 消除了這一點：私鑰永遠不離開發行者，公鑰公開，驗證端能檢查每一個 token，卻無法偽造任何一個。

Key rotation follows from the same property and is the part people forget. Rotating an HS256 secret means updating every service holding it at the same moment, because a token signed with the new secret fails anywhere the old one is still deployed. Under RS256 the issuer publishes its public keys at a JWKS endpoint, each with a key ID that signed tokens carry in their header, so a verifier fetches the key the token names. Rotation becomes publishing a new key and letting the tokens signed with the old one expire, nothing needs redeploying, and what is being distributed is public anyway, so a copy of it leaking costs nothing.

金鑰輪替是同一個性質的延伸，也是最多人忘記的一段。要輪替 HS256 的密鑰，代表所有持有它的服務必須同一時間更新，因為用新密鑰簽出的 token，在任何還留著舊密鑰的地方都會驗不過。在 RS256 底下，發行者把公鑰發布在 JWKS endpoint 上，每一把都帶一個 key ID，簽出的 token 會在標頭裡寫上它，驗證端就去抓 token 指名的那一把。輪替於是變成「發布一把新鑰匙，讓用舊鑰匙簽的 token 自然過期」，沒有東西需要重新部署，而且被散布出去的本來就是公開資訊，外流一份也沒有代價。

The attack that makes this a favourite interview question is algorithm confusion. If the verifier reads the algorithm out of the token's own header, an attacker can take a server configured for RS256, rewrite the header to say HS256, and sign the token using that server's public key as the HMAC secret - and the public key is, by definition, something they are allowed to have. The server then verifies an HMAC against the same value and accepts a token the attacker wrote. The older variant is `alg: none`, where the token simply claims it needs no signature. Both have the same one-line fix: the server states which algorithms it accepts and rejects everything else, instead of letting the token specify how it should be checked. Separately, an HS256 secret has to be long and random, because a token is an offline artifact - anyone holding one can brute-force a weak secret on their own hardware, where nothing rate-limits them.

讓這題成為面試常客的攻擊叫做 algorithm confusion。如果驗證端是從 token 自己的標頭讀出演算法，攻擊者就能拿一台設定為 RS256 的伺服器，把標頭改寫成 HS256，再用那台伺服器的公鑰當作 HMAC 的密鑰去簽 —— 而公鑰按定義就是他有權取得的東西。伺服器接著用同一個值去驗 HMAC，於是接受了一個由攻擊者撰寫的 token。更早的變種是 `alg: none`，token 直接宣稱自己不需要簽章。兩者的修法是同一行：由伺服器聲明它接受哪些演算法並拒絕其餘一切，而不是讓 token 指定自己該怎麼被檢查。另外，HS256 的密鑰必須夠長且隨機，因為 token 是一個離線的產物 —— 任何拿到一個 token 的人，都能在自己的機器上暴力破解弱密鑰，那裡沒有任何東西會對他限速。

So my default is RS256, or ES256 where signature size matters, as soon as anything outside the issuing service verifies tokens, and HS256 only where one service both issues and checks them, with a secret out of a random generator rather than a string someone typed into a config file. Performance is almost never the deciding factor, which is worth saying out loud because it is the reason candidates usually give: an HMAC check costs microseconds and an RSA verification tens of microseconds, and both vanish next to a single database round trip. With RSA the cost that is real is signing rather than verifying, and it lands on the login path instead of on every request.

所以我的預設是：只要有簽發服務以外的東西需要驗證 token，就用 RS256，或在意簽章大小時改用 ES256；只有在同一個服務既簽發又驗證時才用 HS256，而且密鑰要來自亂數產生器，不是某個人手打進設定檔的字串。效能幾乎不會是決定因素，這點值得說出來，因為那正是多數應徵者給的理由：HMAC 檢查是微秒等級，RSA 驗證是數十微秒，兩者擺在一次資料庫來回旁邊都會消失。以 RSA 來說，真正比較貴的是簽章而不是驗證，而它落在登入那條路徑上，不是落在每一個請求上。

## Quick Reference

### The trade, row by row

| | HS256 | RS256 |
|---|---|---|
| Key | One shared secret | A private/public key pair |
| Signing | The secret | The private key, issuer only |
| Verifying | The same secret | The public key, anyone |
| Who can forge a token | Everyone who can verify one | Only the holder of the private key |
| What you distribute | A secret, to every verifier | A public key, to anyone who asks |
| Rotation | Update every holder at once | Publish a new key; old tokens expire |
| Signature size | 32 bytes | 256 bytes at RSA-2048 |
| Cost | Microseconds either way | Verify is cheap; signing is the slow side |
| Use when | One service issues and verifies | Anything else verifies |

### The algorithms you will be asked to place

| `alg` | Family | Key | Note |
|---|---|---|---|
| `HS256` / `HS384` / `HS512` | HMAC | Shared secret | Verifier can also sign |
| `RS256` | RSA PKCS#1 v1.5 | Key pair | The common default for identity providers |
| `PS256` | RSA-PSS | Key pair | Newer padding, preferred over `RS256` for new systems |
| `ES256` | ECDSA P-256 | Key pair | Same guarantee as `RS256`, far smaller signature |
| `EdDSA` | Ed25519 | Key pair | Fast and small; support is less universal |
| `none` | - | - | Unsigned. Never acceptable from a client |

### Verifying an asymmetric token, safely

Pin the algorithm, and look the key up by the `kid` the token names rather than by whatever the token supplies:

```python
import jwt
from jwt import PyJWKClient

jwks = PyJWKClient("https://issuer.example.com/.well-known/jwks.json")

def verify(token: str) -> dict:
    signing_key = jwks.get_signing_key_from_jwt(token).key   # chosen by kid
    return jwt.decode(
        token,
        signing_key,
        algorithms=["RS256"],          # the server decides, not the token
        issuer="https://issuer.example.com",
        audience="orders-api",
    )
```

`algorithms` is the line that stops algorithm confusion. `issuer` and `audience` are the pair that stops a valid token issued for a different service being replayed against this one - a signature check alone only proves the token is genuine, not that it was meant for you.

## Interview Version

> Both produce the same three-part token, and only the third part differs. HS256 is HMAC with SHA-256: a secret is mixed into the hash of the header and payload, and verifying means recomputing it with the same secret. RS256 is an RSA signature over a SHA-256 digest: the issuer signs with a private key and the verifier checks with the matching public key, which cannot sign anything itself. So the question I would actually ask is who has to verify. Under HS256 the verification key is the signing key, so every service that can check a token can also issue one - fine inside a single service that signs and verifies its own tokens, and it is the simpler option there, but the moment a second party verifies you have handed them the power to mint a token for any user. RS256 removes that: the private key stays with the issuer, the public key is published, and a verifier can check every token without being able to forge one. It also makes rotation cheap, because the issuer publishes keys at a JWKS endpoint with a key ID in the token header, so nothing has to be redeployed. The attack to know is algorithm confusion: if the verifier reads the algorithm from the token's header, an attacker rewrites RS256 to HS256 and signs using the server's public key as the HMAC secret, which they are allowed to have. The fix is one line - the server states which algorithms it accepts. So I default to RS256, or ES256 for smaller signatures, whenever anything outside the issuer verifies, and HS256 only for a single service, with a random secret rather than a typed one.

面試時可回答：兩者產出的都是同樣的三段式 token，只有第三段不同。HS256 是 HMAC 搭配 SHA-256：把一把密鑰混進標頭與 payload 的雜湊，驗證就是用同一把密鑰重算一次。RS256 是對 SHA-256 摘要做 RSA 簽章：發行者用私鑰簽，驗證端用對應的公鑰檢查，而公鑰自己簽不出任何東西。所以我真正會問的是：誰需要驗證？在 HS256 底下，驗證的鑰匙就是簽章的鑰匙，因此每個能檢查 token 的服務也都能簽發 token —— 如果簽發與驗證都在同一個服務裡，這沒問題，而且那裡本來就該選比較簡單的它；但只要有第二方要驗，你就把「替任何使用者簽出 token」的能力交了出去。RS256 消除這件事：私鑰留在發行者手上，公鑰公開，驗證端能檢查每一個 token 卻偽造不了任何一個。它也讓輪替變便宜，因為發行者把公鑰放在 JWKS endpoint 上、並在 token 標頭放 key ID，於是什麼都不必重新部署。要知道的攻擊是 algorithm confusion：如果驗證端從 token 標頭讀演算法，攻擊者就把 RS256 改寫成 HS256，並用伺服器的公鑰當 HMAC 密鑰去簽，而公鑰本來就是他能拿到的。修法只有一行 —— 由伺服器聲明它接受哪些演算法。所以我的預設是：只要有發行者以外的東西要驗證就用 RS256、需要小簽章時用 ES256，HS256 只留給單一服務，而且密鑰要用亂數產生，不是手打的。

The sentence to remember is: **Under HS256 anyone who can check a token can also mint one - RS256 is what you reach for the moment that is not acceptable.**

最值得記：**在 HS256 底下，能驗 token 的人就能簽 token —— 一旦這件事不可接受，就換 RS256。**

---

| ⬅ Previous | Home | Next ➡ |
|---|---|---|
| [Q26: What is Cross-Site Request Forgery (CSRF)?](q26-csrf.md) | [All 42 questions](../../README.md) | [Q35: When would you move work onto a message queue?](../architecture-and-scaling/q35-message-queues-and-async-work.md) |
