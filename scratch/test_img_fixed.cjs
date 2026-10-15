const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, ImageRun } = require('docx');

async function testImageFixed() {
    const imgPath = path.join(__dirname, '..', 'week all', 'ui-screens', 'landing-page.png');
    const doc = new Document({
        sections: [{
            children: [
                new Paragraph({
                    children: [
                        new ImageRun({
                            data: fs.readFileSync(imgPath),
                            transformation: { width: 530, height: 295 },
                            type: 'png'
                        })
                    ]
                })
            ]
        }]
    });
    const buf = await Packer.toBuffer(doc);
    fs.writeFileSync('scratch/test_img_fixed.docx', buf);
}

testImageFixed().then(() => console.log('test_img_fixed created'));
