// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ClassVoting {
    // Define Candidate struct
    struct Candidate {
        string prn;
        string name;
    }

    // class ID => candidate PRN => votes
    mapping(string => mapping(string => uint256)) private _votes;

    // class ID => list of candidates
    mapping(string => Candidate[]) private _candidatesPerClass;

    // class ID => candidate PRN => exists?
    mapping(string => mapping(string => bool)) private _candidateExists;

    // voter hash => class ID => has voted?
    mapping(bytes32 => mapping(string => bool)) private _hasVoted;

    constructor() {}

    /** Add candidates to a class. Can be called multiple times per class. */
    function addClassCandidates(string memory classId, Candidate[] memory candidates) external {
        require(candidates.length > 0, "Must provide at least one candidate");

        for (uint256 i = 0; i < candidates.length; ++i) {
            Candidate memory candidate = candidates[i];

            if (!_candidateExists[classId][candidate.prn]) {
                _candidatesPerClass[classId].push(candidate);
                _candidateExists[classId][candidate.prn] = true;
            }
        }
    }

    function candidatesOf(string memory classId)
        external
        view
        returns (Candidate[] memory)
    {
        return _candidatesPerClass[classId];
    }

    function getVotes(string memory classId, string memory candidatePrn)
        external
        view
        returns (uint256)
    {
        _requireValidCandidate(classId, candidatePrn);
        return _votes[classId][candidatePrn];
    }

    /** Anyone can vote — but only once per class. */
    function vote(
        string memory classId,
        string memory candidatePrn,
        string memory voterId
    ) external {
        _requireValidCandidate(classId, candidatePrn);

        bytes32 voterHash = keccak256(abi.encodePacked(voterId));
        require(!_hasVoted[voterHash][classId], "Already voted in this class");

        _hasVoted[voterHash][classId] = true;
        _votes[classId][candidatePrn] += 1;
    }

    function _requireValidCandidate(
        string memory classId,
        string memory candidatePrn
    ) internal view {
        require(_candidateExists[classId][candidatePrn], "Invalid candidate for class");
    }
}
