import React, { useState } from 'react';
import QueryForm from './components/QueryForm';
import ResultsDisplay from './components/ResultsDisplay';
import SettingsModal from './components/SettingsModal';
import { PythonIcon, GearIcon } from './components/icons';
import { generatePythonPackage } from './services/geminiService';
import type { GeneratedFile } from './types';

const App: React.FC = () => {
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [generatedFiles, setGeneratedFiles] = useState<GeneratedFile[]>([]);
    
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);
    const [enhancerModel, setEnhancerModel] = useState('gemini-2.5-flash');
    const [coderModel, setCoderModel] = useState('gemini-2.5-flash');

    const handleGenerate = async (query: string) => {
        setIsLoading(true);
        setError(null);
        setGeneratedFiles([]);
        try {
            const files = await generatePythonPackage(query, coderModel);
            setGeneratedFiles(files);
        } catch (e: any) {
            setError(e.message || "An unexpected error occurred. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleSaveSettings = (settings: { enhancerModel: string; coderModel: string }) => {
        setEnhancerModel(settings.enhancerModel);
        setCoderModel(settings.coderModel);
    };

    return (
        <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col items-center p-4 sm:p-6 md:p-8">
            <header className="w-full max-w-4xl mx-auto text-center mb-8 relative">
                <div className="flex items-center justify-center gap-4 mb-2">
                    <PythonIcon className="w-12 h-12 text-blue-400" />
                    <h1 className="text-4xl sm:text-5xl font-bold text-white tracking-tight">
                        Python Utility Generator
                    </h1>
                </div>
                 <button 
                    onClick={() => setIsSettingsOpen(true)}
                    className="absolute top-0 right-0 p-2 text-gray-400 hover:text-white transition-colors"
                    aria-label="Open settings"
                >
                    <GearIcon className="w-6 h-6" />
                </button>
                <p className="text-lg text-gray-400">
                    Use AI to create modular, self-contained Python packages from a simple description.
                </p>
            </header>
            
            <main className="w-full">
                <QueryForm 
                    onGenerate={handleGenerate} 
                    isLoading={isLoading} 
                    enhancerModel={enhancerModel}
                />
                
                {error && (
                    <div className="mt-8 w-full max-w-4xl mx-auto p-4 bg-red-900/50 border border-red-700 text-red-300 rounded-lg text-center">
                        <p className="font-semibold">An Error Occurred</p>
                        <p>{error}</p>
                    </div>
                )}
                
                {!isLoading && generatedFiles.length > 0 && (
                    <ResultsDisplay files={generatedFiles} />
                )}
            </main>

            <footer className="w-full max-w-4xl mx-auto text-center mt-16 text-gray-500 text-sm">
                <p>Powered by Google Gemini. Generated code is for utility purposes and should be reviewed before use in production.</p>
            </footer>

            <SettingsModal
                isOpen={isSettingsOpen}
                onClose={() => setIsSettingsOpen(false)}
                onSave={handleSaveSettings}
                initialEnhancerModel={enhancerModel}
                initialCoderModel={coderModel}
            />
        </div>
    );
};

export default App;