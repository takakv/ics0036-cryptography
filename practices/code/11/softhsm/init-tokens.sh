#!/bin/sh
set -eu

PIN1=1234
PIN2=12345
PUK=12345678

if [ -n "$(softhsm2-util --show-slots | grep -m1 'Initialized: *yes')" ]; then
    exec "$@"
fi

echo "Creating SoftHSM tokens..."

tmp=$(mktemp -d)
cd "$tmp"

openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:secp384r1 -nodes \
    -keyout ca.key -out ca.crt -days 3650 \
    -subj "/C=EE/O=ICS0036/CN=ICS0036 Test ID Card CA" 2>/dev/null

make_token() {
    token=$1 label=$2 pin=$3 id=$4 usage=$5 x509_usage=$6 subject=$7

    softhsm2-util --init-token --free --label "$token" \
        --pin "$pin" --so-pin "$PUK" > /dev/null

    pkcs11-tool --token-label "$token" --login --pin "$pin" \
        --keypairgen --key-type EC:secp384r1 --label "$label" --id "$id" \
        $usage --sensitive > /dev/null

    pkcs11-tool --token-label "$token" --read-object --type pubkey \
        --id "$id" --output-file pub.der 2> /dev/null
    openssl pkey -pubin -inform DER -in pub.der -out pub.pem

    printf 'keyUsage=critical,%s\nbasicConstraints=CA:FALSE\n' "$x509_usage" > ext.cnf
    openssl x509 -new -force_pubkey pub.pem -subj "$subject" \
        -CA ca.crt -CAkey ca.key -days 1825 -extfile ext.cnf \
        -outform DER -out cert.der 2> /dev/null

    pkcs11-tool --token-label "$token" --login --pin "$pin" \
        --write-object cert.der --type cert --label "$label" --id "$id" > /dev/null
}

subject="/C=EE/O=ESTEID/OU=ICS0036/SN=TUDENG/GN=TEST/serialNumber=PNOEE-50102031232/CN=TUDENG,TEST,50102031232"

make_token "TUDENG,TEST,... (PIN1)" Isikutuvastus "$PIN1" 01 "--usage-sign --usage-derive" \
    "digitalSignature,keyAgreement" "$subject"
make_token "TUDENG,TEST,... (PIN2)" Allkirjastamine "$PIN2" 02 "--usage-sign" \
    "nonRepudiation" "$subject"

cp ca.crt /var/lib/softhsm/tokens/ca.crt

cd /
rm -rf "$tmp"

echo "Done. PIN1 = $PIN1, PIN2 = $PIN2, SO PIN (PUK) = $PUK"
echo
exec "$@"
