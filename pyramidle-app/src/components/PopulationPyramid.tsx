import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import type { PyramidData, AgeGroup } from '../types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface PopulationPyramidProps {
  pyramidData: PyramidData;
  totalPopulation: number;
}

const AGE_GROUPS: AgeGroup[] = [
  '0-4', '5-9', '10-14', '15-19', '20-24', '25-29',
  '30-34', '35-39', '40-44', '45-49', '50-54', '55-59',
  '60-64', '65-69', '70-74', '75-79', '80-84', '85+'
];

export const PopulationPyramid: React.FC<PopulationPyramidProps> = ({
  pyramidData,
  totalPopulation,
}) => {
  // Prepare data for the pyramid chart
  // Male data will be negative (left side), female data positive (right side)
  const maleData = AGE_GROUPS.map(age => -pyramidData.male[age]);
  const femaleData = AGE_GROUPS.map(age => pyramidData.female[age]);

  const data = {
    labels: AGE_GROUPS,
    datasets: [
      {
        label: 'Male',
        data: maleData,
        backgroundColor: 'rgba(54, 162, 235, 0.7)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
      {
        label: 'Female',
        data: femaleData,
        backgroundColor: 'rgba(255, 99, 132, 0.7)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    indexAxis: 'y' as const,
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: `Population Pyramid (Total: ${totalPopulation.toLocaleString()})`,
        font: {
          size: 16,
          weight: 'bold' as const,
        },
      },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            const label = context.dataset.label || '';
            const value = Math.abs(context.parsed.x);
            return `${label}: ${value.toLocaleString()}`;
          },
        },
      },
    },
    scales: {
      x: {
        ticks: {
          callback: function(value: any) {
            // Show absolute values on x-axis
            return Math.abs(value).toLocaleString();
          },
        },
        grid: {
          display: true,
        },
      },
      y: {
        grid: {
          display: false,
        },
      },
    },
  };

  return (
    <div style={{ height: '600px', width: '100%', maxWidth: '800px', margin: '0 auto' }}>
      <Bar data={data} options={options} />
    </div>
  );
};
