import React, { useState, useRef } from 'react';
import ReactDom from 'react-dom';
import './App.css';
import axios from 'axios';


function App() {
  let [barcodeList, setbarcodelist] = useState([]);
  let [barcodeInput, setbarcodeinput] = useState('');
  let [nameInput, setnameinput] = useState('');
  let [pricingList, setpricinglist] = useState([]);
  let [priceInput, setpriceinput] = useState('');
  let [nItemInput, setniteminput] = useState('');
  let [showText, setshowtext] = useState('');
  let [priceText, setpricetext] = useState('Add');
  const n_item_ref = useRef(null);
  const priceRef = useRef(null);


  return (
    <div className="App">
      <a href="/" className="btn btn-light">Back</a>
      <center>
        <br />
        <div>
          {showText === '' ? '' : <div className="alert alert-success" role="alert">Success +1</div>}
        </div>
        <h5>Add Promotion on <a href="/admin/server/promotionongroup/">Group</a></h5>
        <br />
        <div className="flexrow center">
          {/* left */}
          <div className="col-sm-4 barcode-card">
            <h3>Items of {nameInput === '' ? '...' : nameInput}</h3>
            <ol>
              {barcodeList.map((e, i) => <li key={i}>{e}
                <button className="btn btn-danger" onClick={evt => {
                  let arr = barcodeList;
                  const index = arr.indexOf(e);
                  if (index > -1) {
                    arr.splice(index, 1);
                  }
                  setbarcodelist([]);
                  setbarcodelist([...arr]);
                }}>del</button>
              </li>)}
            </ol>
            <div className="flexrow">
              <button onClick={(evt) => {
                setbarcodelist([]);
              }} className="btn btn-warning">ClearAll</button>
              <input value={barcodeInput} onKeyDown={(evt) => {
                if (evt.code == 'Enter' && barcodeInput !== '') {
                  if (!barcodeList.includes(barcodeInput)) {
                    setbarcodelist([...barcodeList, barcodeInput]);
                    setbarcodeinput('');
                  }
                  else {
                    alert('duplicated barcode');
                    setbarcodeinput('');
                  }
                }
              }} onChange={(evt) => setbarcodeinput(evt.target.value)} type="text" className="form-control" placeholder="Scan Barcode" />
              <button onClick={(evt) => {
                if (barcodeInput !== '') {
                  if (!barcodeList.includes(barcodeInput)) {
                    setbarcodelist([...barcodeList, barcodeInput]);
                    setbarcodeinput('');
                  }
                  else {
                    alert('duplicated barcode');
                    setbarcodeinput('');
                  }
                }
              }} className="btn btn-info">Add</button>
            </div>
          </div>

          {/* center */}
          <div className="col-sm-3 center-card">
            <p>Pricing</p>
            <ul>
              {pricingList.map((e, i) => <li key={i}>{e[0]} ชิ้น ราคา {e[1]} บาท

                <button onClick={evt => {

                  let arr = pricingList;
                  const index = arr.indexOf(e);
                  if (index > -1) {
                    arr.splice(index, 1);
                  }
                  setpricinglist([]);
                  setpricinglist([...arr]);
                }} className="btn btn-danger">del</button>
              </li>)}
            </ul>
            <div className="form-group">
              <div className="flexrow">
                <input value={nItemInput} ref={n_item_ref}
                  onChange={evt => setniteminput(evt.target.value)}
                  type="number" name="n_item"
                  onFocus={evt =>
                    setpricetext('Add [Enter]')
                  }
                  onKeyDown={evt => {
                    if (evt.code == 'Enter') {
                      priceRef.current.focus();
                    }
                  }}
                  className="form-control" placeholder="N item" />
              </div>
              <div className="flexrow">
                <input value={priceInput} ref={priceRef} onKeyDown={evt => {
                  if (evt.code == 'Enter') {
                    if (nItemInput !== '' && priceInput !== '') {
                      setpricinglist([...pricingList, [nItemInput, priceInput]]);
                    }
                    else {
                      alert('something went wrong');
                    }
                    setpriceinput('');
                    setniteminput('');
                    n_item_ref.current.focus();
                  }
                }} onFocus={
                  evt => { setpricetext('Add [Enter]'); }
                } onBlur={evt => { setpricetext('Add') }}
                  onChange={evt => {
                    setpriceinput(evt.target.value);
                  }} type="number" name="price" className="form-control" placeholder="Price" />
              </div>
            </div>

            <button onClick={(evt) => {
              // setpricinglist([...pricingList, ['eel', 'ooo']]);
              if (nItemInput !== '' && priceInput !== '') {
                setpricinglist([...pricingList, [nItemInput, priceInput]]);
                setpriceinput('');
                setniteminput('');
              }
            }} className="btn btn-info form-control">{priceText}</button>
          </div>
          {/* right right */}
          <div className="col-sm-2 right-card">
            <div className="flexrow">
              <input type="text" name="name" value={nameInput} onChange={(evt) => setnameinput(evt.target.value)} className="form-control" placeholder="Promotion Name" />
            </div>
            <button onClick={evt => {
              if (barcodeList === [] || pricingList === []) return;
              let data = {
                'name': nameInput,
                'barcode_list': barcodeList,
                'pricing_list': pricingList,
              }
              // setnameinput(data.toString());

              axios.post('/api/promotion-on-group/', data).then((response) => {
                // setnameinput(response.data);
                if (response.status === 200) {
                  // success
                  setshowtext(response.data);
                  // clear text
                  setbarcodelist([]);
                  setpricinglist([]);
                  setnameinput('');
                  setpriceinput('');
                  setniteminput('');
                } else {
                  setshowtext('');
                  alert(response.data);
                }
              })


            }} className="btn btn-primary form-control">Save</button>
          </div>
        </div>
        <br />
        <br />
      </center>
    </div>
  );
}



ReactDom.render(<App />, document.getElementById('app'));