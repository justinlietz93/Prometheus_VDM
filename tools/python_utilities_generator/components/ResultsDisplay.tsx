
import React, { useState, useEffect } from 'react';
import type { GeneratedFile } from '../types';
import { CopyIcon, CheckIcon } from './icons';

interface ResultsDisplayProps {
  files: GeneratedFile[];
}

const FileContentDisplay: React.FC<{ content: string }> = ({ content }) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(content);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="relative font-mono bg-gray-900 border border-gray-700 rounded-b-lg rounded-r-lg">
            <button
                onClick={handleCopy}
                className="absolute top-2 right-2 p-2 bg-gray-700/50 rounded-md hover:bg-gray-600/80 transition-colors duration-200 text-gray-300"
                aria-label="Copy code to clipboard"
            >
                {copied ? <CheckIcon className="w-5 h-5 text-green-400" /> : <CopyIcon className="w-5 h-5" />}
            </button>
            <pre className="p-4 text-sm overflow-x-auto text-gray-200">
                <code className="language-python">{content}</code>
            </pre>
        </div>
    );
};


const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ files }) => {
  const [activeTab, setActiveTab] = useState(0);

  useEffect(() => {
    // Reset to the first tab when files change
    setActiveTab(0);
  }, [files]);
  
  if (files.length === 0) {
    return null;
  }

  return (
    <div className="w-full max-w-4xl mx-auto mt-12">
        <h2 className="text-2xl font-bold text-center mb-6 text-gray-200">Generated Python Package</h2>
        <div>
            <div className="border-b border-gray-700">
                <nav className="-mb-px flex space-x-2" aria-label="Tabs">
                    {files.map((file, index) => (
                        <button
                            key={file.fileName}
                            onClick={() => setActiveTab(index)}
                            className={`whitespace-nowrap py-3 px-4 border-b-2 font-medium text-sm transition-colors duration-200
                                ${activeTab === index 
                                    ? 'border-blue-500 text-blue-400' 
                                    : 'border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-500'
                                }
                            `}
                        >
                            {file.fileName}
                        </button>
                    ))}
                </nav>
            </div>

            <div className="mt-2">
              {files.length > 0 && activeTab < files.length && (
                <FileContentDisplay content={files[activeTab].fileContent} />
              )}
            </div>
        </div>
    </div>
  );
};

export default ResultsDisplay;
