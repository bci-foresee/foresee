import React from 'react';
import { ModulesIcon } from '../Icons/icons';

export default function Modules() {
  return (
    <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-300 flex flex-col flex-grow">
      <div className="flex items-center mb-4">
        <ModulesIcon />
        <h2 className="text-lg font-semibold ml-2">Modules</h2>
      </div>

      <div className="border border-gray-300 p-6 rounded-lg shadow-sm flex flex-col items-center justify-center text-center cursor-pointer hover:border-red-600 transition flex-grow">
          <div className="text-red-600 text-3xl mb-2">
            <img src="/icons/import.png" alt="import icon" className="h-6 w-6" />
          </div>
          <div className="font-semibold text-base">Import Module</div>
          <p className="text-sm text-gray-600 mt-1">Import an implemented module.</p>
        </div>
    </div>
  );
}