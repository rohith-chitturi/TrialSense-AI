import React from 'react';
import { MedicalTimeline } from './MedicalTimeline';

export const Dashboard: React.FC = () => {
  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">TrialSense AI - Analytics Dashboard</h1>
        <p className="text-gray-600 mt-2">Enterprise Clinical Trial Matching & Eligibility Intelligence</p>
      </header>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Timeline Section */}
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm p-6 border border-gray-200">
          <h2 className="text-xl font-semibold mb-6">Patient Medical Timeline</h2>
          <MedicalTimeline />
        </div>
        
        {/* Explainability & Confidence Section */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
          <h2 className="text-xl font-semibold mb-6">AI Confidence Calibration</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Lab Match</span>
              <span className="font-semibold text-green-600">98%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Medication Match</span>
              <span className="font-semibold text-green-600">95%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Disease Match</span>
              <span className="font-semibold text-yellow-600">89%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Age Match</span>
              <span className="font-semibold text-green-600">100%</span>
            </div>
            
            <div className="mt-6 pt-6 border-t border-gray-100">
              <div className="flex justify-between items-center">
                <span className="text-gray-900 font-bold">Overall Confidence</span>
                <span className="text-2xl font-bold text-blue-600">91%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
