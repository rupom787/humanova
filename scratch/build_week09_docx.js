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
    HeadingLevel,
    BorderStyle,
    ShadingType,
    ImageRun,
    PageBreak,
    Footer,
    Header,
    PageNumber,
    NumberFormat
} = require('docx');

// ==========================================
// COLOR PALETTE CONSTANTS
// ==========================================
const COLOR_PRIMARY = "0284C7";       // Sky Blue
const COLOR_PRIMARY_DARK = "0369A1";  // Dark Blue
const COLOR_SLATE_900 = "0F172A";     // Slate 900
const COLOR_SLATE_800 = "1E293B";     // Slate 800
const COLOR_SLATE_700 = "334155";     // Slate 700
const COLOR_SLATE_600 = "475569";     // Slate 600
const COLOR_SLATE_300 = "CBD5E1";     // Slate 300
const COLOR_SLATE_200 = "E2E8F0";     // Slate 200
const COLOR_SLATE_100 = "F1F5F9";     // Slate 100
const COLOR_SLATE_50 = "F8FAFC";      // Slate 50
const COLOR_WHITE = "FFFFFF";
const COLOR_SUCCESS_BG = "ECFDF5";
const COLOR_SUCCESS_TEXT = "065F46";
const COLOR_WARNING_BG = "FFFBEB";
const COLOR_WARNING_TEXT = "92400E";
const COLOR_NOTSTARTED_BG = "F1F5F9";
const COLOR_NOTSTARTED_TEXT = "475569";

// ==========================================
// HELPER BUILDERS
// ==========================================

function createHeading1(text) {
    return new Paragraph({
        spacing: { before: 360, after: 140 },
        keepWithNext: true,
        children: [
            new TextRun({
                text: "■  " + text,
                font: "Segoe UI",
                size: 26, // 13pt
                bold: true,
                color: COLOR_SLATE_900
            })
        ],
        border: {
            bottom: {
                color: COLOR_PRIMARY,
                space: 4,
                style: BorderStyle.SINGLE,
                size: 12
            }
        }
    });
}

function createHeading2(text) {
    return new Paragraph({
        spacing: { before: 240, after: 100 },
        keepWithNext: true,
        children: [
            new TextRun({
                text: text,
                font: "Segoe UI",
                size: 23, // 11.5pt
                bold: true,
                color: COLOR_PRIMARY_DARK
            })
        ]
    });
}

function createHeading3(text) {
    return new Paragraph({
        spacing: { before: 180, after: 80 },
        keepWithNext: true,
        children: [
            new TextRun({
                text: text,
                font: "Segoe UI",
                size: 21, // 10.5pt
                bold: true,
                color: COLOR_SLATE_800
            })
        ]
    });
}

function createParagraph(text, options = {}) {
    return new Paragraph({
        spacing: { before: options.before || 60, after: options.after || 100, line: 276 }, // 1.15 line spacing
        alignment: options.alignment || AlignmentType.LEFT,
        children: [
            new TextRun({
                text: text,
                font: "Segoe UI",
                size: 21, // 10.5pt
                color: options.color || COLOR_SLATE_700,
                bold: options.bold || false,
                italics: options.italics || false
            })
        ]
    });
}

function createBullet(boldPrefix, bodyText) {
    return new Paragraph({
        bullet: { level: 0 },
        spacing: { before: 40, after: 60, line: 260 },
        children: [
            new TextRun({
                text: boldPrefix + " ",
                font: "Segoe UI",
                size: 21,
                bold: true,
                color: COLOR_SLATE_900
            }),
            new TextRun({
                text: bodyText,
                font: "Segoe UI",
                size: 21,
                color: COLOR_SLATE_700
            })
        ]
    });
}

function createCallout(title, text, type = "primary") {
    const borderColor = type === "warning" ? "F59E0B" : COLOR_PRIMARY;
    const bgColor = type === "warning" ? COLOR_WARNING_BG : COLOR_SLATE_50;
    const textColor = type === "warning" ? COLOR_WARNING_TEXT : COLOR_SLATE_700;

    return new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        rows: [
            new TableRow({
                children: [
                    new TableCell({
                        shading: { fill: bgColor, type: ShadingType.CLEAR },
                        borders: {
                            top: { style: BorderStyle.NONE },
                            bottom: { style: BorderStyle.NONE },
                            right: { style: BorderStyle.NONE },
                            left: { style: BorderStyle.SINGLE, size: 24, color: borderColor }
                        },
                        margins: { top: 140, bottom: 140, left: 180, right: 180 },
                        children: [
                            new Paragraph({
                                spacing: { before: 0, after: 40 },
                                children: [
                                    new TextRun({
                                        text: title,
                                        font: "Segoe UI",
                                        size: 21,
                                        bold: true,
                                        color: COLOR_SLATE_900
                                    })
                                ]
                            }),
                            new Paragraph({
                                spacing: { before: 0, after: 0, line: 260 },
                                children: [
                                    new TextRun({
                                        text: text,
                                        font: "Segoe UI",
                                        size: 20,
                                        italics: true,
                                        color: textColor
                                    })
                                ]
                            })
                        ]
                    })
                ]
            })
        ],
        spacing: { before: 140, after: 180 }
    });
}

function createCodeBlock(codeText) {
    const lines = codeText.split('\n');
    const paras = lines.map(line => new Paragraph({
        spacing: { before: 20, after: 20, line: 220 },
        children: [
            new TextRun({
                text: line,
                font: "Consolas",
                size: 18, // 9pt
                color: "E2E8F0"
            })
        ]
    }));

    return new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        rows: [
            new TableRow({
                children: [
                    new TableCell({
                        shading: { fill: COLOR_SLATE_900, type: ShadingType.CLEAR },
                        borders: {
                            top: { style: BorderStyle.SINGLE, size: 6, color: COLOR_SLATE_800 },
                            bottom: { style: BorderStyle.SINGLE, size: 6, color: COLOR_SLATE_800 },
                            left: { style: BorderStyle.SINGLE, size: 6, color: COLOR_SLATE_800 },
                            right: { style: BorderStyle.SINGLE, size: 6, color: COLOR_SLATE_800 }
                        },
                        margins: { top: 120, bottom: 120, left: 140, right: 140 },
                        children: paras
                    })
                ]
            })
        ],
        spacing: { before: 120, after: 160 }
    });
}

function createStyledTable(headers, rowsData, colWidths = []) {
    const headerRow = new TableRow({
        tableHeader: true,
        children: headers.map((h, i) => new TableCell({
            shading: { fill: COLOR_SLATE_900, type: ShadingType.CLEAR },
            borders: {
                top: { style: BorderStyle.SINGLE, size: 6, color: COLOR_SLATE_300 },
                bottom: { style: BorderStyle.SINGLE, size: 12, color: COLOR_SLATE_900 },
                left: { style: BorderStyle.NONE },
                right: { style: BorderStyle.NONE }
            },
            margins: { top: 100, bottom: 100, left: 120, right: 120 },
            width: colWidths[i] ? { size: colWidths[i], type: WidthType.PERCENTAGE } : undefined,
            children: [
                new Paragraph({
                    spacing: { before: 0, after: 0 },
                    children: [
                        new TextRun({
                            text: h,
                            font: "Segoe UI",
                            size: 19, // 9.5pt
                            bold: true,
                            color: COLOR_WHITE
                        })
                    ]
                })
            ]
        }))
    });

    const bodyRows = rowsData.map((row, rIdx) => {
        const bg = rIdx % 2 === 0 ? COLOR_WHITE : COLOR_SLATE_50;
        return new TableRow({
            children: row.map((cellData, cIdx) => {
                let cellChildren = [];
                if (typeof cellData === 'string') {
                    cellChildren = [
                        new Paragraph({
                            spacing: { before: 0, after: 0, line: 240 },
                            children: [
                                new TextRun({
                                    text: cellData,
                                    font: "Segoe UI",
                                    size: 19,
                                    color: COLOR_SLATE_700
                                })
                            ]
                        })
                    ];
                } else if (Array.isArray(cellData)) {
                    cellChildren = cellData;
                } else if (cellData.badge) {
                    let fill = COLOR_NOTSTARTED_BG;
                    let txtColor = COLOR_NOTSTARTED_TEXT;
                    if (cellData.badge === 'Completed') {
                        fill = COLOR_SUCCESS_BG;
                        txtColor = COLOR_SUCCESS_TEXT;
                    } else if (cellData.badge === 'In Progress' || cellData.badge === 'Active Testing' || cellData.badge === 'Mock Response' || cellData.badge === 'Wiring Charts') {
                        fill = COLOR_WARNING_BG;
                        txtColor = COLOR_WARNING_TEXT;
                    }
                    cellChildren = [
                        new Paragraph({
                            spacing: { before: 0, after: 0 },
                            children: [
                                new TextRun({
                                    text: " " + cellData.badge + " ",
                                    font: "Segoe UI",
                                    size: 18,
                                    bold: true,
                                    color: txtColor
                                })
                            ]
                        })
                    ];
                }

                return new TableCell({
                    shading: { fill: bg, type: ShadingType.CLEAR },
                    borders: {
                        top: { style: BorderStyle.SINGLE, size: 4, color: COLOR_SLATE_200 },
                        bottom: { style: BorderStyle.SINGLE, size: 4, color: COLOR_SLATE_200 },
                        left: { style: BorderStyle.NONE },
                        right: { style: BorderStyle.NONE }
                    },
                    margins: { top: 80, bottom: 80, left: 120, right: 120 },
                    width: colWidths[cIdx] ? { size: colWidths[cIdx], type: WidthType.PERCENTAGE } : undefined,
                    children: cellChildren
                });
            })
        });
    });

    return new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        rows: [headerRow, ...bodyRows],
        spacing: { before: 120, after: 180 }
    });
}

function createScreenshotCard(imageRelPath, caption, metaText) {
    const fullPath = path.join(__dirname, '..', imageRelPath);
    let imageRun;
    if (fs.existsSync(fullPath)) {
        imageRun = new ImageRun({
            data: fs.readFileSync(fullPath),
            transformation: {
                width: 540,
                height: 300
            }
        });
    } else {
        imageRun = new TextRun({
            text: `[Screenshot file not found: ${imageRelPath}]`,
            font: "Segoe UI",
            size: 20,
            color: "EF4444",
            bold: true
        });
    }

    return new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        rows: [
            new TableRow({
                children: [
                    new TableCell({
                        shading: { fill: COLOR_WHITE, type: ShadingType.CLEAR },
                        borders: {
                            top: { style: BorderStyle.SINGLE, size: 6, color: COLOR_SLATE_300 },
                            bottom: { style: BorderStyle.SINGLE, size: 6, color: COLOR_SLATE_300 },
                            left: { style: BorderStyle.SINGLE, size: 6, color: COLOR_SLATE_300 },
                            right: { style: BorderStyle.SINGLE, size: 6, color: COLOR_SLATE_300 }
                        },
                        margins: { top: 120, bottom: 120, left: 140, right: 140 },
                        children: [
                            new Paragraph({
                                alignment: AlignmentType.CENTER,
                                spacing: { before: 0, after: 80 },
                                children: [imageRun]
                            }),
                            new Paragraph({
                                alignment: AlignmentType.CENTER,
                                spacing: { before: 40, after: 40 },
                                children: [
                                    new TextRun({
                                        text: caption,
                                        font: "Segoe UI",
                                        size: 20,
                                        bold: true,
                                        color: COLOR_SLATE_900
                                    })
                                ]
                            }),
                            new Paragraph({
                                alignment: AlignmentType.CENTER,
                                spacing: { before: 0, after: 0 },
                                children: [
                                    new TextRun({
                                        text: metaText,
                                        font: "Segoe UI",
                                        size: 18,
                                        italics: true,
                                        color: COLOR_SLATE_600
                                    })
                                ]
                            })
                        ]
                    })
                ]
            })
        ],
        spacing: { before: 140, after: 180 }
    });
}

// ==========================================
// MAIN DOCUMENT COMPILER
// ==========================================

async function generateReportDocx() {
    console.log("Compiling Week 09 DOCX Report...");

    const doc = new Document({
        styles: {
            default: {
                document: {
                    run: {
                        font: "Segoe UI",
                        size: 21,
                        color: COLOR_SLATE_700
                    }
                }
            }
        },
        sections: [
            // ================= COVER PAGE SECTION =================
            {
                properties: {
                    page: {
                        margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 }
                    }
                },
                children: [
                    new Paragraph({
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 200, after: 40 },
                        children: [
                            new TextRun({
                                text: "NORTHERN UNIVERSITY OF BUSINESS AND TECHNOLOGY KHULNA",
                                font: "Segoe UI",
                                size: 24, // 12pt
                                bold: true,
                                color: COLOR_SLATE_900
                            })
                        ]
                    }),
                    new Paragraph({
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 0, after: 300 },
                        children: [
                            new TextRun({
                                text: "Department of Computer Science and Engineering",
                                font: "Segoe UI",
                                size: 20,
                                color: COLOR_SLATE_600
                            })
                        ],
                        border: {
                            bottom: { style: BorderStyle.SINGLE, size: 8, color: COLOR_SLATE_200, space: 10 }
                        }
                    }),

                    new Paragraph({
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 300, after: 100 },
                        children: [
                            new TextRun({
                                text: "CSE 4204: MOBILE COMPUTING LAB",
                                font: "Segoe UI",
                                size: 22,
                                bold: true,
                                color: COLOR_PRIMARY_DARK
                            })
                        ]
                    }),
                    new Paragraph({
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 100, after: 60 },
                        children: [
                            new TextRun({
                                text: "Week 09 Progress and Integration Report",
                                font: "Segoe UI",
                                size: 36, // 18pt
                                bold: true,
                                color: COLOR_SLATE_900
                            })
                        ]
                    }),
                    new Paragraph({
                        alignment: AlignmentType.CENTER,
                        spacing: { before: 0, after: 300 },
                        children: [
                            new TextRun({
                                text: "Feature Completion, System Integration & Mid-Project Review",
                                font: "Segoe UI",
                                size: 24,
                                italics: true,
                                color: COLOR_PRIMARY
                            })
                        ]
                    }),

                    // Project Box
                    new Table({
                        width: { size: 85, type: WidthType.PERCENTAGE },
                        alignment: AlignmentType.CENTER,
                        rows: [
                            new TableRow({
                                children: [
                                    new TableCell({
                                        shading: { fill: COLOR_SLATE_50, type: ShadingType.CLEAR },
                                        borders: {
                                            top: { style: BorderStyle.SINGLE, size: 6, color: COLOR_SLATE_300 },
                                            bottom: { style: BorderStyle.SINGLE, size: 6, color: COLOR_SLATE_300 },
                                            left: { style: BorderStyle.SINGLE, size: 18, color: COLOR_PRIMARY },
                                            right: { style: BorderStyle.SINGLE, size: 6, color: COLOR_SLATE_300 }
                                        },
                                        margins: { top: 140, bottom: 140, left: 180, right: 180 },
                                        children: [
                                            new Paragraph({
                                                alignment: AlignmentType.CENTER,
                                                spacing: { before: 0, after: 40 },
                                                children: [
                                                    new TextRun({
                                                        text: "🛡️ Project: Humanova",
                                                        font: "Segoe UI",
                                                        size: 26,
                                                        bold: true,
                                                        color: COLOR_SLATE_900
                                                    })
                                                ]
                                            }),
                                            new Paragraph({
                                                alignment: AlignmentType.CENTER,
                                                spacing: { before: 0, after: 0 },
                                                children: [
                                                    new TextRun({
                                                        text: "AI Trust Governance & Multi-Tenant Verification Platform",
                                                        font: "Segoe UI",
                                                        size: 20,
                                                        color: COLOR_SLATE_600
                                                    })
                                                ]
                                            })
                                        ]
                                    })
                                ]
                            })
                        ],
                        spacing: { before: 200, after: 360 }
                    }),

                    // Team Table
                    new Paragraph({
                        spacing: { before: 100, after: 80 },
                        children: [
                            new TextRun({
                                text: "SUBMITTED BY: TEAM 07 (SECTION 8C)",
                                font: "Segoe UI",
                                size: 20,
                                bold: true,
                                color: COLOR_SLATE_900
                            })
                        ]
                    }),
                    createStyledTable(
                        ["Student Name", "Student ID", "Assigned System Role"],
                        [
                            ["MD Robayet Hassan Rupom", "11220320979", "Frontend Architect & Team Leader"],
                            ["Bushra Monzur Moumi", "11220321048", "AI Integration & NLP Pipeline Lead"],
                            ["Aqib Jawwad Nahin", "11220320969", "Backend Architect & Database Manager"]
                        ],
                        [40, 25, 35]
                    ),

                    // Submitted To Table
                    new Paragraph({
                        spacing: { before: 120, after: 80 },
                        children: [
                            new TextRun({
                                text: "SUBMITTED TO:",
                                font: "Segoe UI",
                                size: 20,
                                bold: true,
                                color: COLOR_SLATE_900
                            })
                        ]
                    }),
                    createStyledTable(
                        ["Designation", "Details"],
                        [
                            ["Course Instructor", "Md. Riaz Mahmud"],
                            ["Academic Title", "Assistant Professor, Department of CSE, NUBTK"],
                            ["Submission Date", "August 19, 2026"],
                            ["GitHub Repository", "https://github.com/Rupom090/CSE4204-8C-T07-Humanova"]
                        ],
                        [35, 65]
                    )
                ]
            },

            // ================= MAIN BODY SECTION =================
            {
                properties: {
                    page: {
                        margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 }
                    }
                },
                headers: {
                    default: new Header({
                        children: [
                            new Paragraph({
                                alignment: AlignmentType.RIGHT,
                                spacing: { before: 0, after: 100 },
                                children: [
                                    new TextRun({
                                        text: "Humanova — Week 09 Progress & Integration Report (CSE 4204)",
                                        font: "Segoe UI",
                                        size: 17,
                                        color: COLOR_SLATE_400
                                    })
                                ],
                                border: {
                                    bottom: { style: BorderStyle.SINGLE, size: 4, color: COLOR_SLATE_200, space: 4 }
                                }
                            })
                        ]
                    })
                },
                footers: {
                    default: new Footer({
                        children: [
                            new Paragraph({
                                alignment: AlignmentType.RIGHT,
                                spacing: { before: 100, after: 0 },
                                children: [
                                    new TextRun({
                                        text: "Page ",
                                        font: "Segoe UI",
                                        size: 18,
                                        color: COLOR_SLATE_600
                                    }),
                                    new TextRun({
                                        children: [PageNumber.CURRENT],
                                        font: "Segoe UI",
                                        size: 18,
                                        color: COLOR_SLATE_600
                                    }),
                                    new TextRun({
                                        text: " of ",
                                        font: "Segoe UI",
                                        size: 18,
                                        color: COLOR_SLATE_600
                                    }),
                                    new TextRun({
                                        children: [PageNumber.TOTAL_PAGES],
                                        font: "Segoe UI",
                                        size: 18,
                                        color: COLOR_SLATE_600
                                    })
                                ],
                                border: {
                                    top: { style: BorderStyle.SINGLE, size: 4, color: COLOR_SLATE_200, space: 4 }
                                }
                            })
                        ]
                    })
                },
                children: [
                    // Section 1
                    createHeading1("1. Executive Summary"),
                    createParagraph("By Week 09 of the CSE 4204 Mobile Computing Lab curriculum, Team 07 has reached a critical integration milestone in the development of Humanova—an enterprise-grade, multi-tenant AI Trust Governance & Verification Platform. The primary focus of this milestone is transitioning from standalone, modular codebases into a unified, integrated software application."),
                    createParagraph("The team has successfully established the foundational backend architecture in Laravel 12, modeled 35+ relational database tables with 46 Eloquent models in MySQL 8, engineered token-based authentication with 7-tier Role-Based Access Control (RBAC), and developed a reactive, accessible frontend interface using React 19, TypeScript, Vite, and Tailwind CSS."),

                    createCallout(
                        "⚠️ Engineering Transparency: AI Integration Status",
                        "In strict compliance with academic standards and honest milestone reporting, live AI model inference (OpenAI GPT-4o / Gemini 1.5 Pro) is not yet connected to live external APIs in this submission. The Python FastAPI microservice architecture, claim extraction schemas, and controller endpoints are fully scaffolded, structured, and validated locally with mock payloads in preparation for live API connection in Week 10.",
                        "warning"
                    ),

                    // Section 2
                    createHeading1("2. Project Architecture & System Topology"),
                    createParagraph("Humanova follows a Hybrid SaaS & Distributed AI Middleware Architecture. The presentation layer communicates securely with the Laravel API gateway, which manages identity, authorization, persistence, and dispatches background verification tasks to specialized NLP microservices."),

                    createCodeBlock(`+-------------------------------------------------------------------------+
|                       PRESENTATION LAYER (Frontend)                     |
|  React 19 + TypeScript + Vite + Tailwind CSS + Zustand + Lucide Icons   |
+-------------------------------------------------------------------------+
                                    |
                            HTTPS / JSON REST
                                    |
+-------------------------------------------------------------------------+
|                      API GATEWAY & BACKEND (Laravel 12)                 |
|  - Routing & Middleware (Sanctum Auth, RBAC, Rate Limiting, CORS)       |
|  - Controllers: Auth, Scans, Verifications, Organizations, Providers    |
|  - Domain Logic: Prompt Optimization, Confidence Aggregation, Auditing  |
+-------------------------------------------------------------------------+
         |                                                 |
         v                                                 v
+-----------------------+                         +-----------------------+
|   DATA PERSISTENCE    |                         |  AI NLP MICROSERVICE  |
|  - MySQL 8 Relational |                         |  - FastAPI (Python)   |
|  - Redis Cache/Queue  |                         |  - spaCy / Embeddings |
|  - 46 Eloquent Models |                         |  - Claim Extraction   |
+-----------------------+                         +-----------------------+`),

                    createHeading2("2.1 Core Architectural Principles"),
                    createBullet("Strict Tenant Isolation:", "Every scan, API key, user group, and audit log is strictly partitioned by Organization ID."),
                    createBullet("Stateless API Authentication:", "Secured via Laravel Sanctum Bearer tokens with cryptographic hashing."),
                    createBullet("Decoupled Inference Microservice:", "Heavy natural language processing tasks are isolated in a Python FastAPI microservice to prevent blocking PHP gateway worker threads."),

                    // Section 3
                    new Paragraph({ children: [new PageBreak()] }),
                    createHeading1("3. Feature Completion Checklist & Status"),
                    createParagraph("Below is the comprehensive feature tracking matrix evaluating all deliverables outlined in the approved Project Proposal, SRS, and System Design specifications."),

                    createStyledTable(
                        ["ID", "Feature Name", "Tier", "Status", "Reason / Technical Note", "Target Date"],
                        [
                            ["F-01", "User Registration & Validation", "Auth / API", { badge: "Completed" }, "Email uniqueness, password complexity, tenant workspace creation.", "Aug 12, 2026"],
                            ["F-02", "User Login & Sanctum Token", "Auth / API", { badge: "Completed" }, "Password hash verification and Bearer token issuance.", "Aug 12, 2026"],
                            ["F-03", "User Logout & Revocation", "Auth / API", { badge: "Completed" }, "Token deletion from personal_access_tokens table.", "Aug 13, 2026"],
                            ["F-04", "Role-Based Access Control (RBAC)", "Security", { badge: "Completed" }, "7 distinct user roles and permission gates active.", "Aug 14, 2026"],
                            ["F-05", "Multi-Tenant Org Isolation", "Database", { badge: "Completed" }, "Data segregation by organization_id foreign keys.", "Aug 15, 2026"],
                            ["F-06", "UI Design System & Tokens", "Frontend", { badge: "Completed" }, "Atoms, buttons, badges, typography, dark theme tokens.", "Aug 10, 2026"],
                            ["F-07", "Landing Page & Hero Canvas", "Frontend", { badge: "Completed" }, "Futuristic grid canvas, stats counters, value props.", "Aug 08, 2026"],
                            ["F-08", "Auth Views (Login/Register)", "Frontend", { badge: "Completed" }, "Interactive forms, error alerts, responsive layout.", "Aug 11, 2026"],
                            ["F-09", "User Analytics Dashboard", "Frontend", { badge: "Completed" }, "Scan volume metrics, trust scores, recent logs table.", "Aug 13, 2026"],
                            ["F-10", "Provider API Key Manager", "Frontend", { badge: "Completed" }, "UI for configuring OpenAI, Gemini, DeepSeek keys.", "Aug 14, 2026"],
                            ["F-11", "Community Hallucination Feed", "Frontend", { badge: "Completed" }, "Report cards, upvoting controls, category badges.", "Aug 15, 2026"],
                            ["F-12", "User Profile & Reputation", "Frontend", { badge: "Completed" }, "Reputation score gauge, badges, audit history.", "Aug 15, 2026"],
                            ["F-13", "Super Admin Dashboard UI", "Frontend", { badge: "Completed" }, "System health telemetry, queue rates, verifiers.", "Aug 16, 2026"],
                            ["F-14", "35+ Database Migrations", "Database", { badge: "Completed" }, "Foreign keys, cascades, indexes, JSON payload columns.", "Aug 13, 2026"],
                            ["F-15", "46 Eloquent ORM Models", "Backend", { badge: "Completed" }, "Relationships, scopes, casts, and mutators defined.", "Aug 14, 2026"],
                            ["F-16", "API Route Grouping (40+ routes)", "Gateway", { badge: "Completed" }, "Versioned, throttled, authenticated endpoints.", "Aug 15, 2026"],
                            ["F-17", "Auth State Sync (Zustand)", "Client State", { badge: "In Progress" }, "Hydration working; auto-refresh token logic pending.", "Aug 22, 2026"],
                            ["F-18", "Live Scan Submission Bridge", "Integration", { badge: "In Progress" }, "Form captures input; queue worker response wiring.", "Aug 23, 2026"],
                            ["F-19", "Provider Key AES Encryption", "Security", { badge: "In Progress" }, "CRUD endpoints active; cryptographic hook in test.", "Aug 22, 2026"],
                            ["F-20", "FastAPI Microservice Core", "AI Pipeline", { badge: "In Progress" }, "Endpoints scaffolded; awaiting live transformer models.", "Aug 24, 2026"],
                            ["F-21", "Claim Extraction Logic", "AI Pipeline", { badge: "In Progress" }, "Mock sentence parser active; spaCy NER pending.", "Aug 25, 2026"],
                            ["F-22", "Live LLM Provider Orchestrator", "AI Live API", { badge: "Not Started" }, "Awaiting external API key quota configuration.", "Aug 29, 2026"],
                            ["F-23", "Web Evidence Retrieval Engine", "AI Live API", { badge: "Not Started" }, "Awaiting Serper/Tavily Search API key provisioning.", "Aug 30, 2026"],
                            ["F-24", "Automated PDF Report Export", "Reporting", { badge: "Not Started" }, "Scheduled for end-of-project export milestone.", "Sep 02, 2026"]
                        ],
                        [8, 24, 14, 15, 27, 12]
                    ),

                    // Section 4
                    createHeading1("4. Frontend–Backend Integration Status"),
                    createParagraph("Connecting frontend visual components to backend RESTful endpoints was a primary objective of Week 09. Temporary hardcoded data structures within React have been moved to a unified API client service layer (src/services/api.ts)."),

                    createStyledTable(
                        ["Domain", "Frontend Component", "API Endpoint", "Method", "Integration Status"],
                        [
                            ["Auth", "Register.tsx", "/api/v1/auth/register", "POST", { badge: "Completed" }],
                            ["Auth", "Login.tsx", "/api/v1/auth/login", "POST", { badge: "Completed" }],
                            ["Auth", "Navbar.tsx", "/api/v1/auth/logout", "POST", { badge: "Completed" }],
                            ["Auth", "authStore.ts", "/api/v1/auth/me", "GET", { badge: "Completed" }],
                            ["Organization", "OrganizationView.tsx", "/api/v1/organizations", "GET", { badge: "Completed" }],
                            ["API Keys", "ApiKeysView.tsx", "/api/v1/provider-keys", "GET/POST", { badge: "Active Testing" }],
                            ["Scans", "VerificationWorkspace.tsx", "/api/v1/scans", "POST", { badge: "Mock Response" }],
                            ["Reports", "CommunityFeed.tsx", "/api/v1/reports", "GET/POST", { badge: "Active Testing" }],
                            ["Analytics", "DashboardHome.tsx", "/api/v1/analytics/dashboard", "GET", { badge: "Wiring Charts" }]
                        ],
                        [15, 25, 28, 12, 20]
                    ),

                    // Section 5
                    new Paragraph({ children: [new PageBreak()] }),
                    createHeading1("5. User Authentication, Session Management & RBAC"),
                    createParagraph("The authentication layer is fully operational and secured using Laravel Sanctum. The flow enforces cryptographic password validation and issues scoped Bearer tokens stored in localStorage."),

                    createCodeBlock(`+-----------+       +-------------------+       +--------------------+       +----------------------+
|  Client   | ----> | POST /auth/login  | ----> | Laravel Sanctum    | ----> | MySQL \`users\` &      |
| Form View | <---- | 200 OK + Bearer   | <---- | Password Check &   | <---- | \`roles\` Tables       |
+-----------+       | Token + User Dict |       | Token Generation   |       +----------------------+
      |             +-------------------+       +--------------------+
      v
+---------------------------------------------------------------------------------------------------+
|  Client Storage: LocalStorage & Zustand Store                                                     |
|  Protected Route Guard: <ProtectedRoute allowedRoles={['admin', 'researcher', 'user']} />         |
+---------------------------------------------------------------------------------------------------+`),

                    createHeading2("5.1 Role-Based Access Control (RBAC) Matrix"),
                    createStyledTable(
                        ["Role Name", "Level", "Run Scans", "Submit Reports", "Vote", "Moderation Queue", "Manage Keys", "Super Admin"],
                        [
                            ["Guest", "0", "❌", "❌", "❌", "❌", "❌", "❌"],
                            ["User", "1", "✅", "✅", "✅", "❌", "❌", "❌"],
                            ["Researcher", "2", "✅", "✅", "✅", "❌", "❌", "❌"],
                            ["Trusted Verifier", "3", "✅", "✅", "✅", "✅", "❌", "❌"],
                            ["Moderator", "4", "✅", "✅", "✅", "✅", "❌", "❌"],
                            ["Organization Admin", "5", "✅", "✅", "✅", "❌", "✅", "❌"],
                            ["Super Admin", "6", "✅", "✅", "✅", "✅", "✅", "✅"]
                        ],
                        [22, 10, 11, 13, 10, 14, 10, 10]
                    ),

                    // Section 6
                    createHeading1("6. AI Integration Status & Staging Architecture"),
                    createParagraph("Humanova's AI verification engine is engineered as a dedicated Python FastAPI microservice to handle claim extraction, similarity analysis, and contradiction detection independently from the core PHP backend."),

                    createCallout(
                        "Technical Roadmap: Why Live AI is Staged for Week 10",
                        "During Week 09, our primary focus was stabilizing the database, authentication, and REST API foundation. Connecting to live LLM APIs (OpenAI, Gemini) at this stage would incur unnecessary token costs and rate-limiting issues during rapid UI iteration. The microservice endpoints currently return deterministic test schemas, ensuring seamless live integration in Week 10.",
                        "warning"
                    ),

                    createCodeBlock(`+─────────────────────────────────────────────────────────────────────────────+
|                  FASTAPI PYTHON AI MICROSERVICE (Port 8001)                 |
|                                                                             |
|  1. POST /extract-claims        ──> Splits input into atomic testable claims|
|  2. POST /retrieve-evidence     ──> Queries indexed web evidence (Staged)   |
|  3. POST /analyze-similarity    ──> Semantic alignment scoring (Staged)     |
|  4. POST /detect-contradiction  ──> Natural Language Inference (NLI) (Staged)|
+─────────────────────────────────────────────────────────────────────────────+
         |
         v  (JSON Output)
 [Laravel Confidence Engine] ──> Calculates Weighted Trust Score (0-100%)
         |
         v
 [React UI Presentation]     ──> Visual Claim Highlighting & Source Overlays`),

                    // Section 7
                    new Paragraph({ children: [new PageBreak()] }),
                    createHeading1("7. Major End-to-End User Workflows"),
                    createHeading2("7.1 Workflow A: User Authentication & Workspace Access"),
                    createParagraph("The user registers or logs in with validated credentials, receives an encrypted Sanctum Bearer token, hydates client Zustand state, and is securely routed to their personalized analytics dashboard with active role permissions."),

                    createHeading2("7.2 Workflow B: Content Verification & Fact Auditing (Core Path)"),
                    createParagraph("The user inputs AI text into the Verification Workspace. The frontend dispatches a scan request to the Laravel API, which registers the scan record and invokes the Python NLP microservice to extract individual claims, perform citation cross-referencing, compute confidence metrics, and render interactive highlighted claim overlays."),

                    createHeading2("7.3 Workflow C: Community Hallucination Reporting & Peer Verification"),
                    createParagraph("Users flag unverified AI responses through the Community Feed. The submission enters a moderation queue where Trusted Verifiers and Moderators approve or reject the report, updating the shared knowledge base and awarding reputation points to the submitter."),

                    createHeading2("7.4 Workflow D: Multi-Tenant Provider API Key Governance"),
                    createParagraph("Organization Admins configure third-party AI provider keys (OpenAI, Gemini) with model allowances and token limits. The keys are encrypted via AES-256 and stored securely, allowing team members to execute verifications without exposing raw credentials."),

                    // Section 8 & 9
                    createHeading1("8. UI/UX Refinements & Design System"),
                    createBullet("Dynamic Claim Highlighting:", "Overlays visually categorize text into 🟢 Verified, 🟡 Uncertain, and 🔴 Hallucination."),
                    createBullet("Responsive Viewport Scaling:", "Fluid CSS grid layouts adapt seamlessly from mobile (375px) to desktop (1920px)."),
                    createBullet("Shimmer Skeletons:", "Eliminated visual layout shifts during asynchronous network fetches."),
                    createBullet("Form Usability & Validation:", "Live field alerts and disabled submit states prevent duplicate form submissions."),

                    createHeading1("9. Error Handling & Fault Tolerance"),
                    createStyledTable(
                        ["Scenario", "Detection Point", "HTTP Status", "User-Facing Feedback Message"],
                        [
                            ["Invalid Input", "Client Form Validation", "N/A (Client)", "Please enter a valid email and a password with at least 8 characters."],
                            ["Expired Session", "Sanctum Middleware", "401 Unauthorized", "Your session has expired. Redirecting to login..."],
                            ["Forbidden Role", "RBAC Route Gate", "403 Forbidden", "Access Denied: You do not have permission to view this resource."],
                            ["Rate Limit Exceeded", "API Throttle Guard", "429 Too Many Req", "Rate limit reached. Please wait 60 seconds before scanning again."],
                            ["Database Offline", "Backend Core Handler", "503 Service Unavail", "The service is temporarily experiencing database connectivity issues."],
                            ["NLP Microservice Timeout", "Gateway Guzzle Client", "504 Gateway Timeout", "Verification engine timed out. Scan queued for background processing."]
                        ],
                        [18, 20, 18, 44]
                    ),

                    // Section 10 & 11
                    new Paragraph({ children: [new PageBreak()] }),
                    createHeading1("10. Scope Review & Architectural Deviations"),
                    createStyledTable(
                        ["Component", "Original Plan", "Current Implementation", "Reason for Deviation"],
                        [
                            ["Backend Core", "Monolithic Python Flask", "Laravel 12 API Gateway + FastAPI", "Laravel provides superior ORM, RBAC, and rate limiting; FastAPI excels at NLP."],
                            ["Database", "12 Flat Tables", "35+ Tables (46 Models)", "Expanded to support multi-tenancy, audit logs, and claim-level evidence trees."],
                            ["Frontend", "Standard React + Webpack", "React 19 + TypeScript + Vite + Tailwind", "Vastly superior build performance, strict type safety, and modern styling."],
                            ["Tenancy", "Single User Accounts", "Multi-Tenant Org Workspaces", "Enables real-world deployment for university labs and enterprise research teams."]
                        ],
                        [16, 22, 28, 34]
                    ),

                    createHeading1("11. Mid-Project Review & Team Contributions"),
                    createStyledTable(
                        ["Student Name & ID", "Assigned Role", "Key Deliverables Completed", "Progress"],
                        [
                            [
                                "MD Robayet Hassan Rupom\n11220320979",
                                "Frontend Architect & Team Leader",
                                "• Built 10+ core responsive React 19 views.\n• Configured React Router v7 and client route guards.\n• Developed Zustand stores for auth and scan state.\n• Designed claim highlighting overlays and design tokens.",
                                "92%"
                            ],
                            [
                                "Bushra Monzur Moumi\n11220321048",
                                "AI Integration Lead",
                                "• Designed Python FastAPI microservice architecture.\n• Formulated claim extraction and NLI contradiction models.\n• Designed prompt enhancement logic and variation metrics.\n• Built evaluation test fixtures for Week 10 LLM integration.",
                                "85%"
                            ],
                            [
                                "Aqib Jawwad Nahin\n11220320969",
                                "Backend Architect & Database Lead",
                                "• Authored 35+ MySQL database migrations and 46 models.\n• Implemented Laravel Sanctum token auth & password hashing.\n• Configured 7-tier RBAC and multi-tenant organization scopes.\n• Exposed 40+ RESTful API endpoints with throttling.",
                                "95%"
                            ]
                        ],
                        [24, 20, 46, 10]
                    ),

                    // Section 12: Screenshots
                    new Paragraph({ children: [new PageBreak()] }),
                    createHeading1("12. System Interface Screenshots & Demonstrations"),
                    createParagraph("The following verified screenshots illustrate the working user interfaces and functional modules of the Humanova platform."),

                    createScreenshotCard(
                        "week all/ui-screens/landing-page.png",
                        "Figure 12.1: Humanova Public Landing Page & Platform Overview",
                        "File: src/pages/Home.tsx | Features: Animated Hero Canvas, Stats Counter, Value Proposition"
                    ),

                    createScreenshotCard(
                        "week all/ui-screens/register-page.png",
                        "Figure 12.2: User Registration & Workspace Creation Interface",
                        "File: src/pages/auth/Register.tsx | Endpoint: POST /api/v1/auth/register | Features: Live validation"
                    ),

                    new Paragraph({ children: [new PageBreak()] }),
                    createScreenshotCard(
                        "week all/ui-screens/login-page.png",
                        "Figure 12.3: User Login & Session Token Acquisition Portal",
                        "File: src/pages/auth/Login.tsx | Endpoint: POST /api/v1/auth/login | Features: Bearer token generation"
                    ),

                    createScreenshotCard(
                        "week all/ui-screens/dashboard.png",
                        "Figure 12.4: Central Analytics & Verification Telemetry Dashboard",
                        "File: src/pages/dashboard/DashboardHome.tsx | Features: Scan counters, token savings, audit table"
                    ),

                    new Paragraph({ children: [new PageBreak()] }),
                    createScreenshotCard(
                        "week all/ui-screens/verification-page.png",
                        "Figure 12.5: AI Verification Workspace & Fact Extraction Engine",
                        "File: src/pages/verification/VerificationWorkspace.tsx | Features: Claim overlays, confidence score"
                    ),

                    createScreenshotCard(
                        "week all/ui-screens/report-page.png",
                        "Figure 12.6: Community Hallucination Feed & Evidence Inspection",
                        "File: src/pages/community/CommunityFeed.tsx | Features: Peer report cards, upvoting, category badges"
                    ),

                    new Paragraph({ children: [new PageBreak()] }),
                    createScreenshotCard(
                        "week all/ui-screens/api-key-page.png",
                        "Figure 12.7: Multi-Provider API Key Governance Interface",
                        "File: src/pages/settings/ApiKeysView.tsx | Features: Encrypted key storage, monthly token quotas"
                    ),

                    createScreenshotCard(
                        "week all/ui-screens/organization-page.png",
                        "Figure 12.8: Multi-Tenant Workspace & Team Member Management",
                        "File: src/pages/settings/OrganizationView.tsx | Features: Member directory, role assignments"
                    ),

                    new Paragraph({ children: [new PageBreak()] }),
                    createScreenshotCard(
                        "week all/ui-screens/admin-dashboard.png",
                        "Figure 12.9: Super Admin Telemetry & System Health Dashboard",
                        "File: src/pages/dashboard/AdminDashboard.tsx | Features: Queue latency, platform health, moderation queue"
                    ),

                    // Section 13, 14, 15
                    createHeading1("13. GitHub Repository Hygiene & Commit Activity"),
                    createParagraph("The repository is actively maintained with structured git practices, meaningful commit messages, and secret isolation (https://github.com/Rupom090/CSE4204-8C-T07-Humanova)."),

                    createCodeBlock(`* 9558b69 (HEAD -> main, origin/main) feat: complete Phase 1-10 backend architecture, RBAC, and security hardening
* 0837210 feat: Add backend service implementation, docker configurations, and update main repository documentation
* 30d5f0e feat: add application source code and public assets
* d429ce5 feat: add initial UI mockup components and layouts
* 267cf45 docs: update README folder structure and remove Instructions.json
* 9d0e01b docs: rewrite README.md and LICENSE to production-grade quality
* ec197b7 chore: initial repository commit and project scaffolding`),

                    createHeading1("14. Testing, QA & Week 10 Preparation"),
                    createStyledTable(
                        ["Test ID", "Scope", "Procedure", "Expected Result", "Status"],
                        [
                            ["TC-AUTH-01", "Auth", "Register with valid details.", "User inserted in DB; Sanctum token returned.", { badge: "Completed" }],
                            ["TC-AUTH-02", "Auth", "Register with duplicate email.", "HTTP 422 Unprocessable Entity error.", { badge: "Completed" }],
                            ["TC-AUTH-03", "Auth", "Login with invalid password.", "HTTP 401 Unauthorized returned.", { badge: "Completed" }],
                            ["TC-RBAC-01", "Security", "Standard user accesses /admin.", "HTTP 403 Forbidden; view blocked.", { badge: "Completed" }],
                            ["TC-UI-01", "UI/UX", "Resize viewport to 375px width.", "Mobile navigation drawer activates smoothly.", { badge: "Completed" }]
                        ],
                        [16, 14, 30, 30, 10]
                    ),

                    createHeading1("15. Conclusion"),
                    createParagraph("The Week 09 milestone marks substantial progress for Humanova. The foundational backend, relational database architecture, authentication security, and frontend user interface are fully established. With the AI microservice endpoints structured and ready, the team is fully prepared for Week 10 live model integration and formal testing."),

                    createParagraph("Report authored and submitted by Team 07 (Humanova) — CSE 4204: Mobile Computing Lab, Northern University of Business and Technology Khulna.", { italics: true, color: COLOR_SLATE_600 })
                ]
            }
        ]
    });

    const outputPath = path.join(__dirname, '..', 'week all', 'CSE4204-8C-T07_Week09Progress.docx');
    const buffer = await Packer.toBuffer(doc);
    fs.writeFileSync(outputPath, buffer);
    console.log("Successfully generated DOCX at: " + outputPath);
    console.log("File size: " + buffer.length + " bytes");
}

generateReportDocx().catch(err => {
    console.error("Error generating DOCX:", err);
});
