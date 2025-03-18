import React from "react";
import {useRouter} from "next/navigation";
import { PipelineCreatorIcon } from "./icons";


export default function PipelineCreator() {
  const router = useRouter();
  
  return (
    <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-300 md:col-span-2 flex flex-col flex-grow">
      <div className="flex items-center mb-4">
        <PipelineCreatorIcon />
        <h2 className="text-lg font-semibold ml-3">Pipeline Creator</h2>
      </div>
      
      {/* Ensure grid takes full height and centers content */}
      <div className="grid grid-cols-2 gap-4 flex-grow h-full">
        {/* Button 1 */}
        <div className="border border-gray-300 p-6 rounded-lg shadow-sm flex flex-col items-center justify-center text-center cursor-pointer hover:border-red-600 transition flex-grow"
          onClick={() => router.push(`/creation`)}>
          <div className="text-red-600 text-3xl mb-2">+</div>
          <div className="font-semibold text-base">Custom Pipeline</div>
          <p className="text-sm text-gray-600 mt-1">Build a pipeline from scratch.</p>
        </div>

        {/* Button 2 */}
        <div className="border border-gray-300 p-6 rounded-lg shadow-sm flex flex-col items-center justify-center text-center cursor-pointer hover:border-red-600 transition flex-grow">
          <div className="text-red-600 text-3xl mb-2">
            <img src="/icons/import.png" alt="import icon" className="h-6 w-6" />
          </div>
          <div className="font-semibold text-base">Import Pipeline</div>
          <p className="text-sm text-gray-600 mt-1">Import an existing pipeline.</p>
        </div>
      </div>
    </div>
  );
};