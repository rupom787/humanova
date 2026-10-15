const fs = require('fs');
const filePath = 'D:/Dev folder/research-hub-ui/README.md';
let content = fs.readFileSync(filePath, 'utf8');

const topNotice = `# Research Hub Platform

<p align="left">
  <img src="https://img.shields.io/badge/License-Proprietary%20%2F%20All%20Rights%20Reserved-red?style=flat-square" alt="Proprietary License" />
</p>

> [!IMPORTANT]
> **Proprietary Notice & Terms of Access:** This project is published strictly for demonstration, evaluation, and review purposes. All rights are reserved by Rupom Hossain. Any unauthorized reproduction, downloading, cloning, distribution, or reuse of this code or its architecture is strictly prohibited by law. See [LICENSE](LICENSE) for details.

`;

content = content.replace(/# Research Hub Platform\r?\n/, topNotice);

const bottomLicense = `

---

## 📄 License & Intellectual Property

This project is proprietary software — see the [LICENSE](LICENSE) file for complete terms.

\`\`\`
Proprietary & Confidential © 2026 Rupom Hossain (rupom787). All Rights Reserved.
Viewing permitted for evaluation and portfolio review only. Reproduction or distribution strictly prohibited.
\`\`\`
`;

if (!content.includes('## 📄 License & Intellectual Property')) {
  content = content.trimEnd() + bottomLicense;
}

fs.writeFileSync(filePath, content, 'utf8');
console.log('Successfully updated D:/Dev folder/research-hub-ui/README.md');
