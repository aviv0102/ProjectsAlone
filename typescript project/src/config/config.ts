
interface ConfigInfo {
    port: number;
}
type Config = { [env: string]: ConfigInfo }
const Env: string = process.env.NODE_ENV?.toString()  || 'Local' ;


const config: Config = {
    Local: {
        port: 4000,
    },

    Prod: {
        port: 50,
    },
};


export const currentConfig = config[Env];

console.log(process.env.NODE_ENV?.toString() )
console.log(currentConfig)
