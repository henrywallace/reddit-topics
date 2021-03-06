var testjson = {
  nodes: [
    { data: {id: 't1', name: 'topic 1',type: 'topic', } },
    { data: {id: 't2', name: 'topic 2',type: 'topic', } },
    { data: {id: 't3', name: 'topic 3',type: 'topic', } },
    { data: {id: 'w1', name: 'word 1', parent: 't1',type: 'word',} },
    { data: {id: 'w2', name: 'word 2', parent: 't1',type: 'word',} },
    { data: {id: 'w3', name: 'word 3', parent: 't1',type: 'word',} },
  ],
    edges: [
    { data: {id: 'e1', source: 't1', target: 't2', weight: 0.3,type: 'topic', } },
    { data: {id: 'e2',source: 't1', target: 't1', weight: 0.7,type: 'topic', } },
    { data: {id: 'e3',source: 't2', target: 't2', weight: 0.9,type: 'topic', } },
    { data: {id: 'e4',source: 't2', target: 't3', weight: 0.1,type: 'topic', } },
    { data: {id: 'e5',source: 't3', target: 't1', weight: 0.5,type: 'topic', } },
    { data: {id: 'e6',source: 't3', target: 't2', weight: 0.5,type: 'topic', } },
    { data: {id: 'we1',source: 'w1',target: 'w2', weight: 0.4,type: 'word', } },
    { data: {id: 'we2',source: 'w1',target: 'w3', weight: 0.6,type: 'word', } },
    { data: {id: 'we3',source: 'w2',target: 'w3', weight: 1,type: 'word', } },
    { data: {id: 'we4',source: 'w3',target: 'w3', weight: 1,type: 'word', } },
  ]
};