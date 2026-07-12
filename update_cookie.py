import re

curl_cmd = r"""curl ^"https://allafrica.com/search/advanced.html^" ^
  -H ^"accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7^" ^
  -H ^"accept-language: en-US,en;q=0.9^" ^
  -H ^"cache-control: max-age=0^" ^
  -b ^"_pctx=^%^7Bu^%^7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIE4AmHgZgEYALP34AGAKwA2XgHZRvABwKZIAL5A; _pcid=^%^7B^%^22browserId^%^22^%^3A^%^22moupebkpiv945wfu^%^22^%^7D; _ga=GA1.1.1032042593.1783455888; cX_G=cx^%^3A2qei0xcvx4f5w2z2yz6h3syya6^%^3A22rff79001f93; FCCDCF=^%^5Bnull^%^2Cnull^%^2Cnull^%^2Cnull^%^2Cnull^%^2Cnull^%^2C^%^5B^%^5B32^%^2C^%^22^%^5B^%^5C^%^22f1ee0b82-9788-42f9-9cb2-cc280941f0cd^%^5C^%^22^%^2C^%^5B1783461693^%^2C81000000^%^5D^%^5D^%^22^%^5D^%^5D^%^5D; __lxG__consent__v2=1^%^7C1783525822^%^7C1783468800000^%^7C166^%^7C1791301822421^%^7C2^%^7C1^%^7C1^%^7C1783468800000^%^7C1^%^7C17835258072204842^%^7C1^%^7C194^%^7C^%^7C1111111^%^7C^%^7C1^%^7C0^%^7C0^%^7C1^%^7C; __lxG__consent__v2_daisybit=CQnB74AQnB74AA_AFAENCmFsAP_gAEPgAAAALuJB7C7NbWFCwDJ3YLsAcAgDxdAAQsQAAASAAGABQAKQIAQCg0EQBASABAACABAAICRBIQAkCAAQAEAAAIAAKAAEIAAAQAAIAAAAgBAAAgAAAAACAIAAGAAIAgIAEgAAmAgEAAIAGEAAgAACAAAgAAAAAAAAAAAAAAAAAAAAAAAAACAAAQAAgAAAAAAAABAIAAAAAAAAACAAAAgAAAAAQAAAAAAAAAAAACAAAAAAAAAAAiAAAAAAAACAAAAAQXcSD2F2a2sKFgGCuwXYAYBAni6AAhYgAAAkAAMACgAUgQAgFJoIgCAEAAAAAACAAQAiCQABQAAAAAIAAAQAAUAAIAAAAgAAQAAABACAABAAAAAAEAQAAMAAQAAQAIAABEhAIAAQAMIAAAAAEQABAAQAAAAAAAAAAAAAAAAAAAAAAAEAAAAABAAAAAAAAACAQAAAAAAAAAEAAABAAAAAAgAAAAAAAAAAAAEAAAAAIAAAAhEAAAAAAAAEAAAAAgAA.ILuJB7C7NbWFCwDJ3YLsAcAgTxdAAQsQAAASAAGABQAKQIAQCk0EQBASABAACABAAICRBIQAsCAAQAEAAAIAAKAAEIAAAQAAIAAAAgBAAAgAAAAACAIAAGAAIAgIAEgAAmQgEAAIAGEAAgAACIAAgAIAAAAAAAAAAAAAAAAAAAAAAACAAAQAAgAAAAAAAABAIAAAAAAAAACAAAAgAAAAAQAAAAAAAAAAAACAAAAAEAAAAQiAAAAAAAACAAAAAQAA.f_wAD_wAAAAA; __lxG__consent__v2_gdaisybit=~2~70..19.4.15..14..27..47..63..52..12..92..71.81.45..34..290..117..70..44.2.108..71..25..114..34..121.7.74..65..154.8.11..183.2.179..273..42.34.102..513.~; newsletter-signup-inread-english-v1=^{^%^22showCount^%^22:2^%^2C^%^22closeCount^%^22:0^%^2C^%^22successCount^%^22:0^%^2C^%^22timestamp^%^22:1783525823036^}; FCOEC=^%^5B^%^5B^%^5B28^%^2C^%^22^%^5Bnull^%^2C^%^5Bnull^%^2C4^%^2C^%^5B1783461694^%^2C978733000^%^5D^%^2C0^%^5D^%^5D^%^22^%^5D^%^5D^%^5D; FCNEC=^%^5B^%^5B^%^22AKsRol9OpEnpG06yj7g7BIrb9I6ak0yez8datPdlmfjNYicOCcoQNtZ_etl5RPZXRNG5Lljj8yZK0feL9Q7mYH21hLQB3GNFUZIohMHuFFBtX-wk3Yz971Ugs1JUancUAbnwQlwpeaFmQ9PB7cigfmB7nep1XpGaEQ^%^3D^%^3D^%^22^%^5D^%^2Cnull^%^2C^%^5B^%^5B21^%^2C^%^22^%^5B^%^5B^%^5B^%^5B5^%^2C1^%^2C^%^5B8^%^5D^%^5D^%^2C^%^5B1783461694^%^2C887365000^%^5D^%^2C^%^5B1209600^%^5D^%^5D^%^5D^%^5D^%^22^%^5D^%^5D^%^5D; __gads=ID=3cf8ac0b91694ca5:T=1778111032:RT=1783847139:S=ALNI_MYXcg044-J9JUnG2zDg_2eG1d6y7A; __gpi=UID=0000136edba4fe62:T=1778111032:RT=1783847139:S=ALNI_MaVN96BW3AFKaKoyaAw4d9ZncUvYw; __eoi=ID=37aa1349589dbe6c:T=1778111032:RT=1783847139:S=AA-AfjbIF6Kke_zWb4mJEaoIe27r; authn=3KGijzhXv8Z9R2cz4pD74VNhbHRlZF9fDRmWlmqwYrXVUuvRu7JDvV4nyxo8g^%^252Brz45XYWz^%^252FUVMaB^%^250A8KIqxFf7iUq3sfgyGEXuXTHkU^%^252B3onsVmrYUzD1iNtVbm3KN2QAngPs9fbHN2llVfg19jWzg^%^252B3N1L^%^250AxMh2gXpdtyY048cMf882g9cp5MGSRGdPaGpSVPwP^%^250A; authn_subscription=BIGBIVfjk1fg^%^252BxchTNrWDFNhbHRlZF9fzpQgn1g4wW2S75lP^%^252FWQhgHtYBoLwnMQZ5V1mscNeI2T2^%^250A2aqvtNSkg6hCo2qLE0hOCnEq^%^252Fx80OSJRzGFSK5tPN9vavgD^%^252BTYNIjwORFnO1GiZKF1yPfWcHv8De^%^250Ad^%^252FnXzHqxDdaxXG55aeIMzG69xSCuyHBFwlU3ZOMTZPgQy5ZWYbATXzszFdR3sg^%^253D^%^253D^%^250A; _ga_5P8RKMB865=GS2.1.s1783847130^$o17^$g1^$t1783847157^$j60^$l0^$h0; cX_P=moupebkpiv945wfu^" ^"""

match = re.search(r'-b \^"([^"]+)\^"', curl_cmd)
if match:
    cookie_str = match.group(1)
    cookie_str = cookie_str.replace('^%^', '%').replace('^{', '{').replace('^}', '}').replace('^$', '$').replace('^', '')

    secrets_path = r'c:\Users\ayo\Desktop\Grants_Alignment\scripts\secrets.py'
    new_content = f'''# !! DO NOT COMMIT THIS FILE !!
# This file is in .gitignore — it contains your personal browser session cookies.
# To refresh: copy the cookie string from your browser's DevTools Network tab (Request Headers > Cookie).

ALLAFRICA_COOKIES = (
    "{cookie_str}"
)
'''
    with open(secrets_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Cookie updated successfully.")
else:
    print("Could not extract cookie from curl command.")
