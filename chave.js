import crypto from 'crypto';

const newHexKey = crypto.randomBytes(32).toString('hex');
console.log('Nova chave privada hexadecimal:', newHexKey);
