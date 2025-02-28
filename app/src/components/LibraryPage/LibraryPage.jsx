import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import "./LibraryPage.css";

// Icons
const PipelineIcon = () => <div className="icon pipeline-icon">⦿</div>;
const ModulesIcon = () => <div className="icon modules-icon">⚙</div>;
const CustomPipelineIcon = () => <div className="pipeline-card-icon">➕</div>;
const ImportPipelineIcon = () => <div className="pipeline-card-icon">➡</div>;
const ImportModuleIcon = () => <div className="pipeline-card-icon">➕</div>;
const SettingsIcon = () => <div className="settings-icon">⚙</div>;
const ChartIcon = () => <div className="pipeline-action-icon">📊</div>;
const EditIcon = () => <div className="pipeline-action-icon">✏️</div>;

const PipelineCard = ({ title, description, lastRun, icon, selected }) => {
  return (
    <div className={`pipeline-item ${selected ? 'selected' : ''}`}>
      <div className="pipeline-selection">
        <input type="checkbox" checked={selected} readOnly />
      </div>
      <div className="pipeline-content">
        <div className="pipeline-header">
          <div className="pipeline-icon-container">{icon}</div>
          <div className="pipeline-title">{title}</div>
        </div>
        <div className="pipeline-description">{description}</div>
        <div className="pipeline-footer">
          <div className="pipeline-last-run">Last run: {lastRun}</div>
          <div className="pipeline-actions">
            <ChartIcon />
            <EditIcon />
          </div>
        </div>
      </div>
    </div>
  );
};

const CreatorCard = ({ title, description, icon }) => {
  return (
    <div className="creator-card">
      <div className="creator-icon">{icon}</div>
      <div className="creator-title">{title}</div>
      <div className="creator-description">{description}</div>
    </div>
  );
};

const LibraryPage = () => {
  const [pipelines, setPipelines] = useState([
    {
      id: 1,
      title: "Seizure detection 1",
      description: "Data-analytic modeling approach for prediction of epileptic seizures from intracranial EEG recording of brain activity",
      lastRun: "Today",
      icon: <div className="doc-icon">📄</div>,
      selected: true
    },
    {
      id: 2,
      title: "Movement Intent",
      description: "Translates brain signals of movement intent (from intracranial EEG recordings) and communicates with a prosthetic.",
      lastRun: "1/12/25",
      icon: <div className="database-icon">🗃️</div>,
      selected: false
    },
    {
      id: 3,
      title: "Speech decoding",
      description: "A data-driven approach for translating intracranial EEG recordings into speech representations. Decodes neural activity associated with speech production and perception, enabling real-time reconstruction signals.",
      lastRun: "Never",
      icon: <div className="database-icon">🗃️</div>,
      selected: false
    }
  ]);

  const [simulationSettings, setSimulationSettings] = useState({
    power: true,
    latency: false,
    accuracy: false,
    runs: 3
  });

  const [progress, setProgress] = useState(100);

  return (
    <div className="foresee-container">
      <header className="foresee-header">
        <h1>Foresee</h1>
        <p>Create, analyze, and visualize pipelines for novel BCIs with on-device processing.</p>
      </header>

      <div className="grid-container">
        <div className="implemented-pipelines-section">
          <div className="section-header">
            <PipelineIcon />
            <h2>Implemented Pipelines</h2>
            <div className="search-container">
              <input type="text" placeholder="Search pipelines..." className="search-input" />
            </div>
          </div>

          <div className="pipelines-list">
            {pipelines.map(pipeline => (
              <PipelineCard
                key={pipeline.id}
                title={pipeline.title}
                description={pipeline.description}
                lastRun={pipeline.lastRun}
                icon={pipeline.icon}
                selected={pipeline.selected}
              />
            ))}
          </div>
        </div>

        <div className="simulation-section">
          <div className="section-header">
            <SettingsIcon />
            <h2>Simulation Settings</h2>
          </div>

          <div className="simulation-settings">
            <div className="settings-row">
              <div className="setting-option">
                <span>Power</span>
                <div className={`toggle ${simulationSettings.power ? 'active' : ''}`}>
                  <div className="toggle-handle"></div>
                </div>
              </div>
              <div className="setting-option">
                <span>Latency</span>
                <div className={`toggle ${simulationSettings.latency ? 'active' : ''}`}>
                  <div className="toggle-handle"></div>
                </div>
              </div>
            </div>

            <div className="settings-row">
              <div className="setting-option">
                <span>Accuracy</span>
                <div className={`toggle ${simulationSettings.accuracy ? 'active' : ''}`}>
                  <div className="toggle-handle"></div>
                </div>
              </div>
              <div className="setting-option">
                <span>Runs</span>
                <input
                  type="number"
                  className="runs-input"
                  value={simulationSettings.runs}
                  onChange={(e) => setSimulationSettings({...simulationSettings, runs: parseInt(e.target.value) || 0})}
                />
              </div>
            </div>

            <button className="run-button">Run</button>

            <div className="progress-bar-container">
              <div className="progress-bar" style={{ width: `${progress}%` }}></div>
              <div className="progress-value">{progress}%</div>
            </div>

            <div className="simulation-controls">
              <button className="control-button pause">Pause</button>
              <button className="control-button abort">Abort</button>
              <button className="control-button compare">Compare <span>→</span></button>
            </div>
          </div>
        </div>

        <div className="creator-section">
          <div className="section-header">
            <PipelineIcon />
            <h2>Pipeline Creator</h2>
          </div>

          <div className="creator-cards">
            <CreatorCard
              title="Custom Pipeline"
              description="Build a pipeline from scratch."
              icon={<CustomPipelineIcon />}
            />
            <CreatorCard
              title="Import Pipeline"
              description="Import an existing pipeline configuration"
              icon={<ImportPipelineIcon />}
            />
          </div>
        </div>

        <div className="modules-section">
          <div className="section-header">
            <ModulesIcon />
            <h2>Modules</h2>
          </div>

          <div className="creator-cards">
            <CreatorCard
              title="Import a Custom Module"
              description="Import an implemented module."
              icon={<ImportModuleIcon />}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default LibraryPage;