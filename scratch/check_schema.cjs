const fs = require('fs');
const JSZip = require('jszip');

async function checkElements() {
    const data = fs.readFileSync('week all/CSE4204-8C-T07_Week09Progress.docx');
    const zip = await JSZip.loadAsync(data);
    const docXml = await zip.file('word/document.xml').async('string');
    const footerXml = await zip.file('word/footer1.xml').async('string');
    const headerXml = await zip.file('word/header1.xml').async('string');
    
    console.log('--- FOOTER XML ---');
    console.log(footerXml);

    console.log('--- CHECKING PARAGRAPH STRUCTURES ---');
    // Check if any <w:p> contains nested <w:p>
    const nestedP = docXml.match(/<w:p[^>]*>[\s\S]*?<w:p[^>]*>/g);
    console.log('Nested paragraphs in docXml:', nestedP ? nestedP.length : 0);

    // Check if any <w:tc> is empty or missing paragraph
    const emptyTc = docXml.match(/<w:tc[^>]*>\s*<\/w:tc>/g);
    console.log('Empty table cells:', emptyTc ? emptyTc.length : 0);

    // Check drawing tags
    const drawings = docXml.match(/<w:drawing>[\s\S]*?<\/w:drawing>/g);
    console.log('Total drawings:', drawings ? drawings.length : 0);
    if (drawings) {
        drawings.forEach((d, i) => {
            const hasBlip = d.includes('r:embed');
            const hasExtent = d.includes('wp:extent');
            if (!hasBlip || !hasExtent) {
                console.log(`Drawing ${i} missing blip or extent!`);
            }
        });
    }
}

checkElements().catch(console.error);
