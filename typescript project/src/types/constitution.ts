export interface Constitution {
    [key: string]: RuleValue;
}

export interface Rule {
    key: string;
    value: RuleValue;
}

export interface RuleValue {
    geographicScore: string;
    essenceScore: string;
}
