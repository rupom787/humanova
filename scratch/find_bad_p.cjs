const fs = require('fs');
const JSZip = require('jszip');

async function findBadP() {
    const data = fs.readFileSync('week all/CSE4204-8C-T07_Week09Progress.docx');
    const zip = await JSZip.loadAsync(data);
    const docXml = await zip.file('word/document.xml').async('string');
    
    // Find occurrences of <w:p><w:p
    let index = 0;
    while ((index = docXml.indexOf('<w:p', index)) !== -1) {
        const nextP = docXml.indexOf('<w:p', index + 4);
        const endP = docXml.indexOf('</w:p>', index);
        if (nextP !== -1 && nextP < endP) {
            console.log('--- FOUND DIRECT NESTED P AT INDEX', index, '---');
            console.log(docXml.substring(index, nextP + 100));
            break;
        }
        index += 4;
    }
}

findBadP().catch(console.error);
