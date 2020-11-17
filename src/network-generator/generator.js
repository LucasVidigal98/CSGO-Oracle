const fs = require('fs');
const HLTV = require('hltv');
const path = require('path');
const { stringify } = require('querystring');

async function getResult(teamOne, teamTwo, nMatches){
    const infoMatches = await HLTV.HLTV.getTeamStats({id: teamOne});
    const links = {}

    let count = 0;
    let loses = 0;

    console.log('Buscando informações para o time de id = ' + teamOne);

    for(let i=0; i<infoMatches.matches.length; i++){
        try{
            if(infoMatches.matches[i].enemyTeam.id === teamTwo){
                //console.log(infoMatches.matches[i]);
                parsedResult = infoMatches.matches[i].result.split(' ');

                if ((parseInt(parsedResult[0]) - parseInt(parsedResult[2]) < 0)){
                    links[index] = {"loser": teamOne, "winner": teamTwo, "rounds": (parseInt(parsedResult[0]) + parseInt(parsedResult[2]))};
                    loses += 1;
                }

                index = teamOne + '_' + loses;
                //links[index] = infoMatches.matches[i];
                console.log('Encontrado ' + count + ' de '+ nMatches +' resultados contra o time de id = ' + teamTwo);
                console.log('Derrotas encontradas até o momento = ' + loses);
                count += 1;
                if(count === parseInt(nMatches)) break;
                if(i > 1000) break;
            }
        }catch(e){
            console.log('Erro ao encontrar partida: ' + e);
            continue;
        }
    }

    //console.log(links);
    const fileName = './IEM-BEIJING-HAIDIAN-2020-Network-'+ nMatches +'.json';
    const networkData = fs.readFileSync(fileName, 'utf-8');
    const parsedData = JSON.parse(networkData);
    Object.keys(links).map(l => {
        parsedData['Links'].push(links[l]);
    });
    
    const json = JSON.stringify(parsedData);
    fs.writeFile(fileName, json, 'utf8', (err) => {});
}

function addNodes(nodes, nMatches){
    const jsonNetwork = {};
    jsonNetwork['Nodes'] = [];
    jsonNetwork['Links'] = [];
    
    nodes.map(n => {
        jsonNetwork['Nodes'].push(n);
    });

    const fileName = './IEM-BEIJING-HAIDIAN-2020-Network-'+ nMatches +'.json';
    const json = JSON.stringify(jsonNetwork);
    fs.writeFile(fileName, json, 'utf8', (err) => {});
}

async function addLinks(parsedData, nMatches){
    for(let i=0; i<parsedData.data.length; i++){
        let = teamOne = parsedData.data[i].id;
        for(let j=0; j<parsedData.data.length; j++){
            let = teamTwo = parsedData.data[j].id;
            await getResult(teamOne, teamTwo, nMatches);
        }
    }
}



//main
if(process.argv.length > 4 || process.argv.length < 4){
    console.log('Estão faltando parâmetros: Arquivo do campeonato ou número de confrontos máximos!');
    process.exit(1);
}

const data = fs.readFileSync('./IEM-BEIJING-HAIDIAN-2020.json', 'utf-8');
const parsedData = JSON.parse(data);

const nodes = [];
parsedData.data.map(data => {nodes.push({
        "Team_Name": data.name, 
        "id": data.id
    });
});

addNodes(nodes, parseInt(process.argv[3]));
addLinks(parsedData, parseInt(process.argv[3]));