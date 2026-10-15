const fs = require('fs');
const JSZip = require('jszip');

async function inspectImgDocx() {
    const data = fs.readFileSync('scratch/test_img.docx');
    const zip = await JSZip.loadAsync(data);
    console.log('test_img files:', Object.keys(zip.files));
    for (let f in zip.files) {
        if (f.endsWith('.xml') || f.endsWith('.rels')) {
            console.log(`--- ${f} ---`);
            console.log(await zip.file(f).async('string'));
        }
    }
}

inspectImgDocx().catch(console.error);
