const fs = require('fs');
const JSZip = require('jszip');

async function printImgXml() {
    const data = fs.readFileSync('scratch/test_img.docx');
    const zip = await JSZip.loadAsync(data);
    console.log('=== document.xml ===');
    console.log(await zip.file('word/document.xml').async('string'));
    console.log('=== document.xml.rels ===');
    console.log(await zip.file('word/_rels/document.xml.rels').async('string'));
}

printImgXml().catch(console.error);
