import * as server from './src/modules/server';

server.start().then(() => console.log('server is up!'));
