const fs = require('fs');
const HLTV = require('hltv');
const path = require('path');

async function getResult(teamOne, teamTwo, file, nMatches){
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
    const fileName = file + '-' + nMatches +'.json';
    const networkData = fs.readFileSync(path.resolve(__dirname, '..', '..', 'networks', fileName), 'utf-8');
    const parsedData = JSON.parse(networkData);
    Object.keys(links).map(l => {
        parsedData['Links'].push(links[l]);
    });
    
    const json = JSON.stringify(parsedData);
    fs.writeFile(path.resolve(__dirname, '..', '..', 'networks', fileName), json, 'utf8', (err) => {});
}

async function getAllResults(team, file, nMatches, nodes){
    const infoMatches = await HLTV.HLTV.getTeamStats({id: team});
    const links = {}

    let count = 0;
    let loses = 0;

    const fileName = file + '-' + nMatches +'.json';
    const networkData = fs.readFileSync(path.resolve(__dirname, '..', '..', 'networks', fileName), 'utf-8');
    const parsedData = JSON.parse(networkData);
    
    console.log('Buscando informações para o time de id = ' + team);
    
    for(let i=0; i<infoMatches.matches.length; i++){
        try{
            //infoMatches.matches[i].enemyTeam.id
            //console.log(infoMatches.matches[i]);
            parsedResult = infoMatches.matches[i].result.split(' ');
            
            index = team + '_matches_' +count;
            if ((parseInt(parsedResult[0]) - parseInt(parsedResult[2]) < 0)){
                let enemy = infoMatches.matches[i].enemyTeam.id;
                let inNetwork = false;

                parsedData['Links'].map(p=>{
                    if(p.winner === team && p.loser === enemy){
                        inNetwork = true;
                        //break;
                    }
                });

                if(inNetwork) continue;

                links[index] = {"loser": team, "winner": enemy, "rounds": (parseInt(parsedResult[0]) + parseInt(parsedResult[2]))};
                loses += 1;

                inNetwork = true;

                nodes.map(n => {
                    if(n.id === enemy){
                        inNetwork = true; 
                        //break;
                    }
                });
    
                if(inNetwork){
                    let teamName = infoMatches.matches[i].enemyTeam.name
                    nodes.push({
                        "Team_Name": teamName,
                        "id": enemy
                    });
                }
            }else{
                let enemy = infoMatches.matches[i].enemyTeam.id;
                let inNetwork = false;

                parsedData["Links"].map(p=>{
                    if(p.winner === enemy && p.loser === team){
                        inNetwork = true;
                        //break;
                    }
                });

                if(inNetwork) continue;

                links[index] = {"loser": enemy, "winner": team, "rounds": (parseInt(parsedResult[0]) + parseInt(parsedResult[2]))};
                loses += 1;

                inNetwork = true;

                nodes.map(n => {
                    if(n.id === enemy){
                        inNetwork = true; 
                        //break;
                    }
                });
    
                if(inNetwork){
                    let teamName = infoMatches.matches[i].enemyTeam.name
                    nodes.push({
                        "Team_Name": teamName,
                        "id": enemy
                    });
                }
            }

            //links[index] = infoMatches.matches[i];
            //console.log('Encontrado ' + count + ' de '+ nMatches +' resultados contra o time de id = ' + teamTwo);
            count += 1;
            console.log('Partida(s) encontradas até o momento = ' + count);
            if(count === parseInt(nMatches)) break;
            if(i > 1000) break;
            
        }catch(e){
            console.log('Erro ao encontrar partida: ' + e);
            continue;
        }
    }

    //console.log(links);
    Object.keys(links).map(l => {
        parsedData['Links'].push(links[l]);
    });

    parsedData['Nodes'] = nodes;
    
    const json = JSON.stringify(parsedData);
    fs.writeFile(path.resolve(__dirname, '..', '..', 'networks', fileName), json, 'utf8', (err) => {});
}

function addNodes(nodes, file, nMatches){
    const jsonNetwork = {};
    jsonNetwork['Nodes'] = [];
    jsonNetwork['Links'] = [];
    
    nodes.map(n => {
        jsonNetwork['Nodes'].push(n);
    });

    const fileName = file + '-' + nMatches +'.json';
    const json = JSON.stringify(jsonNetwork);
    fs.writeFile(path.resolve(__dirname, '..', '..', 'networks', fileName), json, 'utf8', (err) => {});
}

async function addLinks(parsedData, file, nMatches){
    for(let i=0; i<parsedData.data.length; i++){
        let = teamOne = parsedData.data[i].id;
        for(let j=0; j<parsedData.data.length; j++){
            let = teamTwo = parsedData.data[j].id;
            await getResult(teamOne, teamTwo, file, nMatches);
        }
    }
}

async function addAllLinks(parsedData, file, nMatches, nodes){
    for(let i=0; i<parsedData.data.length; i++){
        let team = parsedData.data[i].id;
        await getAllResults(team, file, nMatches, nodes);
    }
}



//main
if(process.argv.length > 5 || process.argv.length < 5){
    console.log('Estão faltando parâmetros: Arquivo do campeonato ou número de confrontos máximos!');
    process.exit(1);
}

const data = fs.readFileSync(path.resolve(__dirname, '..', 'championships', process.argv[2] + '.json'), 'utf-8');
const parsedData = JSON.parse(data);

const nodes = [];
parsedData.data.map(data => {nodes.push({
        "Team_Name": data.name, 
        "id": data.id
    });
});

addNodes(nodes, process.argv[2], parseInt(process.argv[3]));
if(process.argv[4] == 0)
    addLinks(parsedData, process.argv[2], parseInt(process.argv[3]));
else
    addAllLinks(parsedData, process.argv[2], process.argv[3], nodes);