import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  CartesianGrid
} from "recharts";

function PriceChart({ timeline, highest, lowest, average }) {
  if (!timeline || timeline.length === 0) return null;

  return (
    <div className="card">
      <h3>📈 Price History</h3>

      {/* STATS */}
      <div className="stats">
        <div>
          <span>⬆ Highest</span>
          <strong>₹{highest}</strong>
        </div>
        <div>
          <span>⬇ Lowest</span>
          <strong>₹{lowest}</strong>
        </div>
        <div>
          <span>📊 Avg</span>
          <strong>₹{average}</strong>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={timeline}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip
            formatter={(v) => `₹${v}`}
            labelStyle={{ fontWeight: "bold" }}
          />

          {/* Reference Lines */}
          <ReferenceLine
            y={lowest}
            stroke="#22c55e"
            strokeDasharray="4 4"
            label="Lowest"
          />
          <ReferenceLine
            y={average}
            stroke="#facc15"
            strokeDasharray="4 4"
            label="Average"
          />
          <ReferenceLine
            y={highest}
            stroke="#ef4444"
            strokeDasharray="4 4"
            label="Highest"
          />

          <Line
            type="monotone"
            dataKey="price"
            stroke="#2563eb"
            strokeWidth={3}
            dot={{ r: 4 }}
            activeDot={{ r: 7 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default PriceChart;
