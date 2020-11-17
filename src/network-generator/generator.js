const fs = require('fs');
const HLTV = require('hltv');
const { get } = require('http');
const { parse } = require('path');

async function getResult(teamOne, teamTwo){
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

                if (parsedResult[0] < 16){
                    links[index] = {"loser": teamOne, "winner": teamTwo, "rounds": (parseInt(parsedResult[0]) + parseInt(parsedResult[2]))};
                    loses += 1;
                }else{
                    //Verfica se foi para prorrogação e se perdeu a prorrogação
                    if((parsedResult[0] - parsedResult[2]) < 0){
                        links[index] = {"loser": teamOne, "winner": teamTwo, "rounds": (parseInt(parsedResult[0]) + parseInt(parsedResult[2]))};
                        loses += 1;
                    }
                }

                index = teamOne + '_' + loses;
                //links[index] = infoMatches.matches[i];
                console.log('Encontrado ' + count + ' 10 resultados contra o time de id = ' + teamTwo);
                console.log('Derrotas encontradas até o momento = ' + loses);
                count += 1;
                if(count === 10) break;
                if(i > 1000) break;
            }
        }catch(e){
            console.log('Erro ao encontrar partida: ' + e);
            continue;
        }
    }

    //console.log(links);
    const networkData = fs.readFileSync('./IEM-BEIJING-HAIDIAN-2020-Network.json', 'utf-8');
    const parsedData = JSON.parse(networkData);
    Object.keys(links).map(l => {
        parsedData['Links'].push(links[l]);
    });
    
    const json = JSON.stringify(parsedData);
    fs.writeFile('./IEM-BEIJING-HAIDIAN-2020-Network.json', json, 'utf8', (err) => {});
}

function addNodes(nodes){
    const jsonNetwork = {};
    jsonNetwork['Nodes'] = [];
    jsonNetwork['Links'] = [];
    
    nodes.map(n => {
        jsonNetwork['Nodes'].push(n);
    });

    const json = JSON.stringify(jsonNetwork);
    fs.writeFile('./IEM-BEIJING-HAIDIAN-2020-Network.json', json, 'utf8', (err) => {});
}

async function addLinks(parsedData){
    for(let i=0; i<parsedData.data.length; i++){
        let = teamOne = parsedData.data[i].id;
        for(let j=0; j<parsedData.data.length; j++){
            let = teamTwo = parsedData.data[j].id;
            await getResult(teamOne, teamTwo);
        }
    }
}

const data = fs.readFileSync('./IEM-BEIJING-HAIDIAN-2020.json', 'utf-8');
const parsedData = JSON.parse(data);

const nodes = [];
parsedData.data.map(data => {nodes.push({
        "Team_Name": data.name, 
        "id": data.id
    });
});

addNodes(nodes);
addLinks(parsedData);
