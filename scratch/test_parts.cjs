const fs = require('fs');
const path = require('path');
const {
    Document,
    Packer,
    Paragraph,
    TextRun,
    Table,
    TableRow,
    TableCell,
    WidthType,
    AlignmentType,
    BorderStyle,
    ImageRun,
    PageBreak,
    Footer,
    Header,
    PageNumber
} = require('docx');

// Test 1: Just Header and Footer
async function testHeaderFooter() {
    const doc = new Document({
        sections: [{
            headers: {
                default: new Header({
                    children: [
                        new Paragraph({
                            alignment: AlignmentType.RIGHT,
                            children: [
                                new TextRun("Header test")
                            ]
                        })
                    ]
                })
            },
            footers: {
                default: new Footer({
                    children: [
                        new Paragraph({
                            alignment: AlignmentType.RIGHT,
                            children: [
                                new TextRun("Page "),
                                new TextRun({ children: [PageNumber.CURRENT] }),
                                new TextRun(" of "),
                                new TextRun({ children: [PageNumber.TOTAL_PAGES] })
                            ]
                        })
                    ]
                })
            },
            children: [
                new Paragraph({ children: [new TextRun("Hello World")] })
            ]
        }]
    });
    const buf = await Packer.toBuffer(doc);
    fs.writeFileSync('scratch/test_hf.docx', buf);
}

// Test 2: Image
async function testImage() {
    const imgPath = path.join(__dirname, '..', 'week all', 'ui-screens', 'landing-page.png');
    const doc = new Document({
        sections: [{
            children: [
                new Paragraph({
                    children: [
                        new ImageRun({
                            data: fs.readFileSync(imgPath),
                            transformation: { width: 530, height: 295 }
                        })
                    ]
                })
            ]
        }]
    });
    const buf = await Packer.toBuffer(doc);
    fs.writeFileSync('scratch/test_img.docx', buf);
}

Promise.all([testHeaderFooter(), testImage()]).then(() => console.log('Tests generated.'));
