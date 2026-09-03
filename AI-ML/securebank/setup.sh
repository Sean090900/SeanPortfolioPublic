echo "DOWNLOADING DATA SOURCES...saving files to '../securebank/data_sources'"
mkdir -p securebank/data_sources

echo " > Downloading fraud_release.json"
wget --no-check-certificate \
    "https://www.dropbox.com/scl/fi/l7hbax6q9l46litljsp2z/fraud_release.json?rlkey=rki4elqxt7fwpg1pqqfjfp4of&st=w2dwjsrc&dl=1" \
    -O securebank/data_sources/fraud_release.json

echo " > Downloading customer_release.csv"
wget --no-check-certificate \
    "https://www.dropbox.com/scl/fi/gkzdmeajx9nd9tkzwzoxs/customer_release.csv?rlkey=g2ssbe0dhuszz066v5phg27pn&st=yb0ggzjo&dl=1" \
    -O securebank/data_sources/customer_release.csv

echo " > Downloading transactions_release.parquet"
wget --no-check-certificate \
    "https://www.dropbox.com/scl/fi/ym1wvmja0b2tblgtzxypj/transactions_release.parquet?rlkey=3nx1a75ss8tip3sdlhoq62j9r&st=30rqa81w&dl=1" \
    -O securebank/data_sources/transactions_release.parquet
