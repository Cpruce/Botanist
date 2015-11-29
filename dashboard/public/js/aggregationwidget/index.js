import React from 'react';
import { render } from 'react-dom';
import PieChart, BarChart, AreaChart from '../c3charts/index.js';


const examples = (
  <div>
    <PieChart />
    <BarChart />
    <AreaChart />
  </div>
);

render(examples, document.getElementById('aggregation-container'));
