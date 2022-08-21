import axios from 'axios';
import { useProjectStore } from '../stores/project';
import { nextTick } from 'vue';

export async function downloadObjects(objects, context, tablePrefix='') {
    for (let objName in objects) {
        // objName must match a sql table name (with prefix, if needed)
        // console.log('download for ' + objName);
        if (typeof(context[objName]) != 'object' || context[objName].length == 0) {
            continue;
        }
        const attributes = Object.keys(context[objName][0])
        const tableName = tablePrefix + objName;
        const filterClause = tableName.startsWith('lu_') ? '' : 'prj_id=' + useProjectStore().prj_id  
        context[objName] = await downloadObject(tableName,attributes,filterClause);
    }
}

export async function downloadObject(tableName, attributes, filterClause = '', LOG = false) {
    const objectClause = "?object=" + tableName;
    // objName must match an object array; only the first element is used to get its attributes 
    const attributesClause = "&attributes=" + attributes.join(',');
    // object / table names starting  with 'lu_' are lookup tables; all others require a prj_id 
    const request = objectClause + attributesClause + (filterClause == '' ? '' : '&' + filterClause); 
    if (LOG) console.log(request);
    const response = await axios.get('https://w75w7350kh.execute-api.us-west-2.amazonaws.com/production/sbcDataService'+ request);
    if (LOG) console.log(response);
    for (let i=0;i<response.data.length;i++) {
        var tempObj = {};
        for (let j=0;j<attributes.length; j++) {
            tempObj[attributes[j]] = response.data[i][j]; 
        }
        response.data[i] = tempObj;
    }
    return response.data;
}

export async function insert(tableName, attributes, userId, LOG = false) {
    const payload = {};
    payload['object'] = tableName;
    attributes['prj_id'] = useProjectStore().prj_id;
    attributes['user_id'] = userId;
    payload['attributes'] = attributes;
    if (LOG) console.log(payload);    
    const response = await axios.post('https://w75w7350kh.execute-api.us-west-2.amazonaws.com/production/sbcDataService',payload);
    const new_id = response.data[0][0];
    return new_id;
}

export async function update(tableName, id, attributes, userId, LOG = false) {
    const payload = {};
    payload['object'] = tableName;
    payload['id'] = id;
    attributes['user_id'] = userId;
    payload['attributes'] = attributes;
    if (LOG) console.log(payload);    
    const response = await axios.put('https://w75w7350kh.execute-api.us-west-2.amazonaws.com/production/sbcDataService',payload);
}

export async function remove(tableName, ids, LOG = false) {
    const payload = {};
    payload['object'] = tableName;
    payload['ids'] = ids;
    if (LOG) console.log(payload);    
    const response = await axios.delete('https://w75w7350kh.execute-api.us-west-2.amazonaws.com/production/sbcDataService',{data:payload});
}
