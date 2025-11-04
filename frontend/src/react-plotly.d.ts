declare module 'react-plotly.js' {
  import { Component } from 'react';
  import { PlotParams } from 'plotly.js';

  export interface PlotProps extends Partial<PlotParams> {
    data: Partial<Plotly.Data>[];
    layout?: Partial<Plotly.Layout>;
    config?: Partial<Plotly.Config>;
    frames?: Partial<Plotly.Frame>[];
    useResizeHandler?: boolean;
    style?: React.CSSProperties;
    className?: string;
    onInitialized?: (figure: Readonly<Plotly.Figure>, graphDiv: Readonly<HTMLElement>) => void;
    onUpdate?: (figure: Readonly<Plotly.Figure>, graphDiv: Readonly<HTMLElement>) => void;
    onPurge?: (figure: Readonly<Plotly.Figure>, graphDiv: Readonly<HTMLElement>) => void;
    onError?: (err: Readonly<Error>) => void;
    divId?: string;
    revision?: number;
    debug?: boolean;
  }

  export default class Plot extends Component<PlotProps> {}
}
