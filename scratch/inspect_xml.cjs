const fs = require('fs');
const JSZip = require('jszip');

async function inspectAllXml() {
    const data = fs.readFileSync('week all/CSE4204-8C-T07_Week09Progress.docx');
    const zip = await JSZip.loadAsync(data);
    for (const [filename, file] of Object.entries(zip.files)) {
        if (filename.endsWith('.xml') || filename.endsWith('.rels')) {
            const content = await file.async('string');
            console.log(`=== FILE: ${filename} (length: ${content.length}) ===`);
            // Check for empty elements or broken tags
            if (filename.includes('document.xml')) {
                // Check if any <w:p> is empty or inside invalid structure
                const invalidParas = content.match(/<w:p\s*\/>/g);
                console.log('Empty self-closing paragraphs:', invalidParas ? invalidParas.length : 0);
                
                // Check table grids
                const tables = content.match(/<w:tbl>[\s\S]*?<\/w:tbl>/g);
                console.log(`Total tables: ${tables ? tables.length : 0}`);
                if (tables) {
                    tables.forEach((t, i) => {
                        const hasGrid = t.includes('<w:tblGrid>');
                        const rows = t.match(/<w:tr[\s>]/g);
                        console.log(`Table ${i}: hasGrid=${hasGrid}, rows=${rows ? rows.length : 0}`);
                    });
                }
            }
        }
    }
}

inspectAllXml().catch(console.error);
