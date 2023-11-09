# purex
for filtering out distgusting contents from x.com via mitmproxy

# steps

- install mitmproxy `brew install mitmproxy`
- install corresponding ca cert
- `mitmproxy --mode upstream:http://127.0.0.1:7890 -s purex.rb` replaced with actual proxy address (optional)
- switch the proxy of the browser to local mitm proxy (default localhost:8080) `SwitchyOmega` preferred
- creating file named `words.txt`, appending some keywords into it
