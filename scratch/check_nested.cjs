const fs = require('fs');
const JSZip = require('jszip');

async function testNestedP() {
    const data = fs.readFileSync('week all/CSE4204-8C-T07_Week09Progress.docx');
    const zip = await JSZip.loadAsync(data);
    const docXml = await zip.file('word/document.xml').async('string');
    
    // Check if any <w:p> has another <w:p> before its closing </w:p>, excluding <w:tc>
    const tcBlocks = docXml.split('<w:tc>');
    let badNested = 0;
    for (let i = 0; i < tcBlocks.length; i++) {
        const block = tcBlocks[i].split('</w:tc>')[0];
        // In a table cell, having multiple <w:p> is fine.
        // But outside <w:tc>, let's check.
    }
    
    // Let's check for <w:p><w:p>
    const directNested = docXml.match(/<w:p[^>]*>\s*<w:p[^>]*>/g);
    console.log('Direct nested <w:p><w:p>:', directNested ? directNested.length : 0);
}

testNestedP().catch(console.error);
