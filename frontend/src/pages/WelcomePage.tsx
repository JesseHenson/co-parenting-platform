import { useState } from 'react';
import TeamSetup from '../components/TeamSetup';
import type { Team } from '../types';

interface Props {
  onComplete: (team: Team) => void;
  onSkip: () => void;
}

const steps = [
  {
    number: '1',
    title: 'Define the Challenge',
    description: 'Describe what your team needs to work through. Everyone reviews and approves the problem statement before moving on.',
    color: 'bg-emerald-100 text-emerald-700',
  },
  {
    number: '2',
    title: 'Brainstorm Ideas',
    description: 'Each teammate contributes ideas independently. Keep private draft notes while you think things through.',
    color: 'bg-sky-100 text-sky-700',
  },
  {
    number: '3',
    title: 'AI-Powered Analysis',
    description: 'When everyone is ready, AI analyzes every idea for pros/cons, feasibility, and fairness — so decisions are balanced.',
    color: 'bg-amber-100 text-amber-700',
  },
];

export default function WelcomePage({ onComplete, onSkip }: Props) {
  const [showSetup, setShowSetup] = useState(false);

  if (showSetup) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
        <div className="max-w-lg w-full">
          <TeamSetup onTeamCreated={onComplete} />
          <button
            onClick={onSkip}
            className="mt-2 w-full text-center text-sm text-slate-500 hover:text-slate-700"
          >
            I'll do this later
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
      <div className="max-w-2xl w-full py-12">
        {/* Welcome header */}
        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Welcome to Greenlight</h1>
          <p className="mt-3 text-lg text-slate-600">
            A structured space for teams to work through decisions together — fairly, calmly, and with AI support.
          </p>
        </div>

        {/* How it works */}
        <div className="bg-white rounded-lg border border-slate-200/60 shadow-sm p-6 mb-8">
          <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-5">How it works</h2>
          <div className="space-y-5">
            {steps.map((step) => (
              <div key={step.number} className="flex items-start gap-4">
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${step.color}`}>
                  {step.number}
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900">{step.title}</h3>
                  <p className="text-sm text-slate-600 mt-0.5">{step.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col items-center gap-3">
          <button
            onClick={() => setShowSetup(true)}
            className="w-full max-w-sm px-6 py-3 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 font-semibold text-center shadow-sm transition-colors"
          >
            Get Started
          </button>
          <button
            onClick={onSkip}
            className="text-sm text-slate-500 hover:text-slate-700"
          >
            Skip — I'll explore on my own
          </button>
        </div>
      </div>
    </div>
  );
}
