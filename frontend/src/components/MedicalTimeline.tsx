import React from 'react';

const timelineEvents = [
  { year: '2018', title: 'Diagnosed Diabetes', type: 'diagnosis' },
  { year: '2020', title: 'Started Metformin', type: 'medication' },
  { year: '2021', title: 'HbA1c 8.5', type: 'lab' },
  { year: '2022', title: 'Kidney Disease', type: 'diagnosis' },
  { year: '2023', title: 'Insulin', type: 'medication' },
  { year: '2026', title: 'Eligible for Trial', type: 'eligibility', highlight: true }
];

export const MedicalTimeline: React.FC = () => {
  return (
    <div className="relative border-l-2 border-blue-200 ml-3">
      {timelineEvents.map((event, index) => (
        <div key={index} className="mb-8 ml-6 relative">
          <span className={`absolute -left-[35px] flex items-center justify-center w-6 h-6 rounded-full ring-4 ring-white ${
            event.highlight ? 'bg-blue-600' : 'bg-blue-100'
          }`}>
            {event.highlight && (
              <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            )}
          </span>
          <h3 className="flex items-center mb-1 text-lg font-semibold text-gray-900">
            {event.title}
            {event.highlight && (
              <span className="bg-blue-100 text-blue-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded ml-3">
                Latest
              </span>
            )}
          </h3>
          <time className="block mb-2 text-sm font-normal leading-none text-gray-400">
            Recorded in {event.year}
          </time>
          <p className="text-base font-normal text-gray-500">
            {event.type === 'diagnosis' ? 'FHIR Condition Resource matched to SNOMED CT / ICD-10.' :
             event.type === 'medication' ? 'FHIR MedicationRequest mapped to RxNorm.' :
             event.type === 'lab' ? 'FHIR Observation resource matched to LOINC.' :
             'AI Recommendation based on multi-level RAG and LangGraph eligibility checking.'}
          </p>
        </div>
      ))}
    </div>
  );
};
