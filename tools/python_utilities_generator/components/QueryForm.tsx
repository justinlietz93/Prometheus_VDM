import React, { useState } from 'react';
import { EXAMPLE_QUERIES } from '../constants';
import { LoadingSpinner, SparklesIcon, PythonIcon } from './icons';
import { enhanceUserPrompt } from '../services/geminiService';

interface QueryFormProps {
    onGenerate: (query: string) => void;
    isLoading: boolean;
    enhancerModel: string;
}

const QueryForm: React.FC<QueryFormProps> = ({ onGenerate, isLoading, enhancerModel }) => {
    const [query, setQuery] = useState('');
    const [isEnhancing, setIsEnhancing] = useState(false);
    const [enhanceError, setEnhanceError] = useState<string | null>(null);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim()) {
            onGenerate(query);
        }
    };

    const handleExampleClick = (exampleQuery: string) => {
        setQuery(exampleQuery);
        // Optionally auto-submit
        // onGenerate(exampleQuery);
    };

    const handleEnhanceClick = async () => {
        if (!query.trim() || isLoading || isEnhancing) return;
        setIsEnhancing(true);
        setEnhanceError(null);
        try {
            const enhancedQuery = await enhanceUserPrompt(query, enhancerModel);
            setQuery(enhancedQuery);
        } catch (e: any) {
            setEnhanceError(e.message || "Failed to enhance prompt. Please try again.");
        } finally {
            setIsEnhancing(false);
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto">
            <form onSubmit={handleSubmit} className="mb-8">
                <div className="relative">
                    <textarea
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Describe the Python utility you want to create..."
                        className="w-full h-40 p-4 bg-gray-800 border border-gray-700 rounded-lg shadow-inner focus:ring-2 focus:ring-blue-500 focus:outline-none resize-y transition-colors duration-200 text-gray-200"
                        disabled={isLoading || isEnhancing}
                    />
                </div>

                {enhanceError && (
                    <div className="mt-2 text-sm text-red-400">
                        <p>{enhanceError}</p>
                    </div>
                )}

                <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
                     <button
                        type="button"
                        onClick={handleEnhanceClick}
                        disabled={isLoading || isEnhancing || !query.trim()}
                        className="w-full flex items-center justify-center px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 disabled:bg-gray-600 disabled:cursor-not-allowed transition-all duration-200"
                    >
                        {isEnhancing ? (
                            <>
                                <LoadingSpinner />
                                <span>Enhancing...</span>
                            </>
                        ) : (
                            <>
                                <SparklesIcon className="w-5 h-5 mr-2" />
                                Enhance Prompt
                            </>
                        )}
                    </button>
                    <button
                        type="submit"
                        disabled={isLoading || isEnhancing || !query.trim()}
                        className="w-full flex items-center justify-center px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed transition-all duration-200"
                    >
                        {isLoading ? (
                            <>
                                <LoadingSpinner />
                                <span>Generating...</span>
                            </>
                        ) : (
                            <>
                                <PythonIcon className="w-5 h-5 mr-2" />
                                Generate Utility
                            </>
                        )}
                    </button>
                </div>
            </form>

            <div>
                <h3 className="text-lg font-semibold text-center text-gray-400 mb-4">Or try one of these examples:</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {EXAMPLE_QUERIES.map((example) => (
                        <button
                            key={example.title}
                            onClick={() => handleExampleClick(example.query)}
                            disabled={isLoading || isEnhancing}
                            className="p-4 bg-gray-800/50 rounded-lg text-left hover:bg-gray-700/70 transition-colors duration-200 disabled:opacity-50 border border-gray-700"
                        >
                            <p className="font-bold text-blue-400">{example.title}</p>
                            <p className="text-sm text-gray-400 mt-1 line-clamp-2">{example.query}</p>
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default QueryForm;