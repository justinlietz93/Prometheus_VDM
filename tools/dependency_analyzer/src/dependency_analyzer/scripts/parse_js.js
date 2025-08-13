const fs = require('fs');
const parser = require('@babel/parser');
const path = require('path');

const filePath = process.argv[2];

if (!filePath) {
    console.error(JSON.stringify({
        provides: [],
        imports: [],
        requires: [],
        uses: [],
        external: [],
        description: "Error: No file path provided"
    }));
    process.exit(1);
}

try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const ast = parser.parse(content, {
        sourceType: 'module',
        plugins: [
            'jsx',
            'typescript',
            'classProperties',
            'objectRestSpread',
            'export/DefaultFrom',
            'dynamicImport',
            'decorators-legacy',
            'classPrivateProperties',
            'optionalChaining',
            'nullishCoalescingOperator'
        ]
    });

    const fileDir = path.dirname(filePath);
    const normalizeImportPath = (importPath) => {
        if (importPath.startsWith('.')) {
            const absolutePath = path.resolve(fileDir, importPath);
            const relativePath = path.relative(process.cwd(), absolutePath).replace(/\\\/g, '/');
            return relativePath.replace(/^frontend\\//, 'frontend.').replace(/\\//g, '.').replace(/\\.js$/, '').replace(/\\.ts$/, '').replace(/\\.tsx$/, '');
        }
        return importPath;
    };

    const imports = [];
    for (const node of ast.program.body) {
        if (node.type === 'ImportDeclaration') {
            const source = node.source.value;
            const normalizedSource = normalizeImportPath(source);
            node.specifiers.forEach(spec => {
                if (spec.type === 'ImportSpecifier' || spec.type === 'ImportDefaultSpecifier' || spec.type === 'ImportNamespaceSpecifier') {
                    if (spec.local) {
                        imports.push({ from: normalizedSource, import: spec.local.name, as: spec.local.name });
                    }
                }
            });
        }
    }

    const requires = [];
    for (const node of ast.program.body) {
        if (node.type === 'ExpressionStatement' &&
            node.expression.type === 'CallExpression' &&
            node.expression.callee.name === 'require' &&
            node.expression.arguments.length > 0 &&
            node.expression.arguments[0].type === 'StringLiteral') {
            const source = node.expression.arguments[0].value;
            requires.push(normalizeImportPath(source));
        }
    }

    const external = new Set([...imports.map(imp => imp.from), ...requires]);

    const provides = [];
    for (const node of ast.program.body) {
        if (node.type === 'ExportNamedDeclaration' && node.declaration) {
            if (node.declaration.type === 'FunctionDeclaration' || node.declaration.type === 'TSEnumDeclaration') {
                provides.push(node.declaration.id.name);
            } else if (node.declaration.type === 'VariableDeclaration') {
                node.declaration.declarations.forEach(decl => {
                    if (decl.id.type === 'Identifier') {
                        provides.push(decl.id.name);
                    }
                });
            } else if (node.declaration.type === 'TSInterfaceDeclaration' || node.declaration.type === 'TSTypeAliasDeclaration') {
                provides.push(node.declaration.id.name);
            }
        } else if (node.type === 'ExportDefaultDeclaration') {
            if (node.declaration.type === 'Identifier') {
                provides.push(node.declaration.name);
            } else if (node.declaration.type === 'FunctionDeclaration' || 
                      node.declaration.type === 'ClassDeclaration' || 
                      node.declaration.type === 'TSInterfaceDeclaration') {
                provides.push('default');
            }
        } else if (node.type === 'ExpressionStatement' &&
                   node.expression.type === 'AssignmentExpression' &&
                   node.expression.left.type === 'MemberExpression' &&
                   node.expression.left.object.name === 'module' &&
                   node.expression.left.property.name === 'exports') {
            if (node.expression.right.type === 'ObjectExpression') {
                node.expression.right.properties.forEach(prop => {
                    if (prop.key.type === 'Identifier') {
                        provides.push(prop.key.name);
                    }
                });
            } else if (node.expression.right.type === 'Identifier') {
                provides.push(node.expression.right.name);
            }
        }
    }

    const uses = new Set();
    const traverse = (node) => {
        if (!node) return;

        if (node.type === 'CallExpression') {
            if (node.callee.type === 'Identifier') {
                uses.add(node.callee.name);
            } else if (node.callee.type === 'MemberExpression') {
                if (node.callee.property.type === 'Identifier') {
                    uses.add(node.callee.property.name);
                }
            }
        }

        if (node.type === 'JSXElement' && node.openingElement.name.type === 'JSXIdentifier') {
            uses.add(node.openingElement.name.name);
        }

        if (node.type === 'TSCallSignatureDeclaration' && node.typeAnnotation) {
            traverse(node.typeAnnotation);
        }

        if (node.type === 'VariableDeclaration') {
            node.declarations.forEach(decl => {
                if (decl.init && decl.init.type === 'CallExpression') {
                    if (decl.init.callee.type === 'Identifier') {
                        uses.add(decl.init.callee.name);
                    } else if (decl.init.callee.type === 'MemberExpression') {
                        if (decl.init.callee.property.type === 'Identifier') {
                            uses.add(decl.init.callee.property.name);
                        }
                    }
                }
            });
        }

        if (node.type === 'AssignmentExpression') {
            const expr = node.right;
            if (expr && expr.type === 'CallExpression') {
                if (expr.callee.type === 'Identifier') {
                    uses.add(expr.callee.name);
                } else if (expr.callee.type === 'MemberExpression') {
                    if (expr.callee.property.type === 'Identifier') {
                        uses.add(expr.callee.property.name);
                    }
                }
            }
        }

        for (const key in node) {
            if (node[key] && typeof node[key] === 'object') {
                if (Array.isArray(node[key])) {
                    node[key].forEach(child => traverse(child));
                } else {
                    traverse(node[key]);
                }
            }
        }
    };

    traverse(ast);

    const result = {
        provides: provides,
        imports: imports,
        requires: requires,
        uses: Array.from(uses),
        external: Array.from(external),
        description: `Handles ${filePath.split('\\\\').pop().split('.')[0]} in ${filePath.split('\\\\').slice(-2)[0]} module.`
    };
    console.log(JSON.stringify(result));
} catch (e) {
    console.error(JSON.stringify({
        provides: [],
        imports: [],
        requires: [],
        uses: [],
        external: [],
        description: `Parse error: ${e.message} at line ${e.loc?.line || 'unknown'}`
    }));
    process.exit(1);
}
