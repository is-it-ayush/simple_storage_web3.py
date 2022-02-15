// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {

    //Data Types
    uint256 favoriteNumber = 10;
    bool favoriteBool = false;
    string favoriteString = "String";
    int256 favoriteInt = -10;
    address favoriteAddress = 0x8865Aa30eBBB7b25674e301b58082b306c1560d3;
    bytes32 favoriteBytes = "cat";

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    //view, pure
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    } 

    //Struct is basically creating a object comprised of other objects or vars.
    struct People {
        uint256 favoriteNumber;
        string name;
    }
    // Using Struct as an array.
    People[] public people;

    function addPersion(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber,_name));        

        //Add to mapping too.
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }


    //------------------------------------------
    // Mapping
    mapping(string => uint256) public nameToFavoriteNumber;
   
}