import Coinkey from 'coinkey';
import * as bitcoin from 'bitcoinjs-lib';
import bs58 from 'bs58'; // Importar o módulo 'bs58'
import crypto from 'crypto';

// Função para converter a chave hexadecimal para WIF manualmente
function hexToWIF(hexKey) {
    try {
        if (!hexKey || typeof hexKey !== 'string') {
            throw new Error("Chave privada inválida.");
        }
        console.log("Chave privada hexadecimal:", hexKey); // Log da chave privada
        const keyBuffer = Buffer.from(hexKey, 'hex');
        console.log("Buffer da chave privada:", keyBuffer); // Log do buffer da chave privada
        if (keyBuffer.length !== 32) {
            throw new Error("A chave privada hexadecimal deve ter 32 bytes de comprimento.");
        }

        const prefix = Buffer.from([0x80]);
        const suffix = Buffer.from([0x01]);
        const extendedKey = Buffer.concat([prefix, keyBuffer, suffix]);

        const checksum = crypto.createHash('sha256').update(extendedKey).digest();
        const doubleChecksum = crypto.createHash('sha256').update(checksum).digest();
        const wifKey = Buffer.concat([extendedKey, doubleChecksum.slice(0, 4)]);

        const wifKeyBase58 = bs58.encode(wifKey); // Usando o módulo 'bs58' para codificar em base58
        console.log("Chave WIF gerada:", wifKeyBase58); // Log da chave WIF gerada
        return wifKeyBase58;
    } catch (e) {
        console.error("Erro ao converter a chave privada para WIF:", e.message);
        return null;
    }
}

// Substitua 'hexKey' por uma chave privada hexadecimal válida de 32 bytes
const hexKey = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'; // Nova chave privada hexadecimal
const wifKey = hexToWIF(hexKey);

if (wifKey) {
    console.log('Chave WIF: ', wifKey);

    let _key = new Coinkey(Buffer.from(hexKey, 'hex'));

    _key.compressed = true;

    console.log('Endereço:', _key.publicAddress);
} else {
    console.error("Erro ao gerar a chave WIF.");
}
