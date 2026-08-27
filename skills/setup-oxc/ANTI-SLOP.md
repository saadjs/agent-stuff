# Anti-slop opt-in

Only when explicitly requested.

```sh
git clone --depth=1 https://github.com/dmmulroy/anti-slop.git <tmp>
git -C <tmp> rev-parse HEAD
```

Read `<tmp>/skills/install-anti-slop/SKILL.md` fully; follow it as current source of truth. From target repo:

```sh
node <tmp>/skills/install-anti-slop/scripts/install.mjs
```

Run upstream checks; report commit/findings; remove `<tmp>`.

Done: every upstream-required rule enabled and checked.
