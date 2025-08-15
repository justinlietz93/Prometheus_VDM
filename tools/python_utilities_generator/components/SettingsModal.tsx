import React, { useState, useEffect } from 'react';

interface SettingsModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSave: (settings: { enhancerModel: string; coderModel: string }) => void;
    initialEnhancerModel: string;
    initialCoderModel: string;
}

const SettingsModal: React.FC<SettingsModalProps> = ({
    isOpen,
    onClose,
    onSave,
    initialEnhancerModel,
    initialCoderModel,
}) => {
    const [enhancerModel, setEnhancerModel] = useState(initialEnhancerModel);
    const [coderModel, setCoderModel] = useState(initialCoderModel);

    useEffect(() => {
        setEnhancerModel(initialEnhancerModel);
        setCoderModel(initialCoderModel);
    }, [initialEnhancerModel, initialCoderModel, isOpen]);

    if (!isOpen) {
        return null;
    }

    const handleSave = () => {
        onSave({
            enhancerModel: enhancerModel.trim() || 'gemini-2.5-flash',
            coderModel: coderModel.trim() || 'gemini-2.5-flash',
        });
        onClose();
    };

    return (
        <div 
            className="fixed inset-0 bg-black bg-opacity-70 z-50 flex justify-center items-center"
            onClick={onClose}
        >
            <div 
                className="bg-gray-800 rounded-lg shadow-xl p-6 w-full max-w-md border border-gray-700"
                onClick={(e) => e.stopPropagation()}
            >
                <h2 className="text-2xl font-bold text-white mb-4">Agent Settings</h2>
                
                <div className="space-y-6">
                    <div>
                        <label htmlFor="enhancer-model" className="block text-sm font-medium text-gray-300 mb-1">
                            Enhance Prompt Agent
                        </label>
                        <p className="text-xs text-gray-400 mb-2">Enter a Gemini Model Name for prompt refinement.</p>
                        <input
                            type="text"
                            id="enhancer-model"
                            value={enhancerModel}
                            onChange={(e) => setEnhancerModel(e.target.value)}
                            placeholder="e.g., gemini-2.5-flash"
                            className="w-full p-2 bg-gray-900 border border-gray-600 rounded-md focus:ring-2 focus:ring-indigo-500 focus:outline-none text-gray-200"
                        />
                    </div>
                    
                    <div>
                        <label htmlFor="coder-model" className="block text-sm font-medium text-gray-300 mb-1">
                            Code Generation Agent
                        </label>
                         <p className="text-xs text-gray-400 mb-2">Enter a Gemini Model Name for code generation.</p>
                        <input
                            type="text"
                            id="coder-model"
                            value={coderModel}
                            onChange={(e) => setCoderModel(e.target.value)}
                            placeholder="e.g., gemini-2.5-flash"
                            className="w-full p-2 bg-gray-900 border border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-200"
                        />
                    </div>
                </div>

                <div className="mt-8 flex justify-end space-x-4">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 bg-gray-600 text-white font-semibold rounded-lg hover:bg-gray-700 transition-colors"
                    >
                        Cancel
                    </button>
                    <button
                        onClick={handleSave}
                        className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
                    >
                        Save Settings
                    </button>
                </div>
            </div>
        </div>
    );
};

export default SettingsModal;